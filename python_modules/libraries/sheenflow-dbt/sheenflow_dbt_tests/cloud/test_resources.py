import re

import pytest
import responses
from sheenflow_dbt import dbt_cloud_resource

from sheenflow import Failure, build_init_resource_context
from sheenflow._check import CheckError

from .utils import (
    SAMPLE_ACCOUNT_ID,
    SAMPLE_API_PREFIX,
    SAMPLE_JOB_ID,
    SAMPLE_RUN_ID,
    sample_job_details,
    sample_list_artifacts,
    sample_run_details,
    sample_run_results,
    sample_runs_details,
)


def get_dbt_cloud_resource(**kwargs):

    return dbt_cloud_resource(
        build_init_resource_context(
            config={"auth_token": "some_auth_token", "account_id": SAMPLE_ACCOUNT_ID, **kwargs}
        )
    )


def test_get_job():

    dc_resource = get_dbt_cloud_resource()

    with responses.RequestsMock() as rsps:
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/",
            json=sample_job_details(),
        )
        assert dc_resource.get_job(SAMPLE_JOB_ID) == sample_job_details()["data"]


@pytest.mark.parametrize(
    "job_id,include_related,query_string",
    [
        (
            345,
            ["environment"],
            "?include_related=%5B%27environment%27%5D&order_by=-id&offset=0&limit=100&job_definition_id=345",
        ),
        (
            None,
            ["environment", "repository"],
            "?include_related=%5B%27environment%27%2C+%27repository%27%5D&order_by=-id&offset=0&limit=100",
        ),
        (None, None, "?include_related=%5B%5D&order_by=-id&offset=0&limit=100"),
    ],
)
def test_get_runs(job_id, include_related, query_string):
    dc_resource = get_dbt_cloud_resource()

    with responses.RequestsMock() as rsps:
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{query_string}",
            json=sample_runs_details(),
        )
        assert (
            dc_resource.get_runs(include_related=include_related, job_id=job_id)
            == sample_runs_details()["data"]
        )


def test_get_run():

    dc_resource = get_dbt_cloud_resource()

    with responses.RequestsMock() as rsps:
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/",
            json=sample_run_details(),
        )
        assert dc_resource.get_run(SAMPLE_RUN_ID) == sample_run_details()["data"]


def test_list_run_artifacts():

    dc_resource = get_dbt_cloud_resource()

    with responses.RequestsMock() as rsps:
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/artifacts/",
            json=sample_list_artifacts(),
        )
        assert dc_resource.list_run_artifacts(SAMPLE_RUN_ID) == sample_list_artifacts()["data"]


def test_get_run_results():
    dc_resource = get_dbt_cloud_resource(request_max_retries=10, request_retry_delay=0)

    with responses.RequestsMock() as rsps:
        for _ in range(9):
            rsps.add(
                rsps.GET,
                f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/artifacts/run_results.json",
                status=500,
            )
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/artifacts/run_results.json",
            json=sample_run_results(),
        )
        assert dc_resource.get_run_results(SAMPLE_RUN_ID) == sample_run_results()


@pytest.mark.parametrize("max_retries,n_flakes", [(0, 0), (1, 2), (5, 7), (7, 5), (4, 4)])
def test_request_flake(max_retries, n_flakes):

    dc_resource = get_dbt_cloud_resource(request_max_retries=max_retries)

    def _mock_interaction():
        with responses.RequestsMock() as rsps:
            for _ in range(n_flakes):
                rsps.add(rsps.GET, f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/", status=500)
            rsps.add(
                rsps.GET, f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/", json=sample_run_details()
            )
            return dc_resource.get_run(SAMPLE_RUN_ID)

    if n_flakes > max_retries:
        with pytest.raises(
            Failure,
            match=re.escape(
                f"Max retries ({max_retries}) exceeded with url: https://cloud.getdbt.com/api/v2/accounts/30000/runs/5000000/."
            ),
        ):
            _mock_interaction()
    else:
        assert _mock_interaction() == sample_run_details()["data"]


def test_no_disable_schedule():

    dc_resource = get_dbt_cloud_resource(disable_schedule_on_trigger=False)
    with responses.RequestsMock() as rsps:
        # endpoint for launching run
        rsps.add(
            rsps.POST, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/run/", json=sample_run_details()
        )
        # run will immediately succeed
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/",
            json=sample_run_details(status_humanized="Success"),
        )
        # endpoint for run_results.json
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/artifacts/run_results.json",
            json=sample_run_results(),
        )
        # endpoint for disabling the schedule has not been set up, so will fail if attempted
        dc_resource.run_job_and_poll(SAMPLE_JOB_ID)


@pytest.mark.parametrize(
    "final_status,expected_behavior",
    [("Success", 0), ("Error", 1), ("Cancelled", 1), ("Running", 2), ("FooBarBaz", 3)],
)
def test_run_job_and_poll(final_status, expected_behavior):
    dc_resource = get_dbt_cloud_resource()
    with responses.RequestsMock() as rsps:
        # endpoint for job details info
        rsps.add(rsps.GET, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/", json=sample_run_details())
        # endpoint for disabling job schedule
        rsps.add(rsps.POST, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/", json=sample_job_details())
        # endpoint for launching run
        rsps.add(
            rsps.POST, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/run/", json=sample_run_details()
        )
        # endpoint for polling run details
        for i in range(10):
            if i == 0:
                status = "Queued"
            elif i == 1:
                status = "Starting"
            elif i < 9:
                status = "Running"
            else:
                status = final_status
            rsps.add(
                rsps.GET,
                f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/",
                json=sample_run_details(status_humanized=status),
            )
        if expected_behavior == 0:
            # endpoint for run_results.json
            rsps.add(
                rsps.GET,
                f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/artifacts/run_results.json",
                json=sample_run_results(),
            )
        if expected_behavior in [2, 3]:
            # endpoint for cancelling run
            rsps.add(
                rsps.POST,
                f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/cancel/",
                json=sample_run_details(),
            )

        def _do_thing():
            return dc_resource.run_job_and_poll(SAMPLE_JOB_ID, poll_interval=0.05, poll_timeout=1)

        if expected_behavior == 0:
            dbt_cloud_output = _do_thing()
            assert dbt_cloud_output.result == sample_run_results()
            assert dbt_cloud_output.run_details == sample_run_details()["data"]
        elif expected_behavior == 1:
            with pytest.raises(Failure, match=f"Run {SAMPLE_RUN_ID} failed"):
                _do_thing()
        elif expected_behavior == 2:
            with pytest.raises(Failure, match=f"Run {SAMPLE_RUN_ID} timed out"):
                _do_thing()
        elif expected_behavior == 3:
            with pytest.raises(CheckError, match=f"Received unexpected status '{final_status}'"):
                _do_thing()


def test_no_run_results_job():
    dc_resource = get_dbt_cloud_resource()
    with responses.RequestsMock() as rsps:
        # endpoint for job details info
        rsps.add(rsps.GET, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/", json=sample_run_details())
        # endpoint for disabling job schedule
        rsps.add(rsps.POST, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/", json=sample_job_details())
        # endpoint for launching run
        rsps.add(
            rsps.POST, f"{SAMPLE_API_PREFIX}/jobs/{SAMPLE_JOB_ID}/run/", json=sample_run_details()
        )
        # endpoint for polling run details
        for i in range(10):
            if i == 0:
                status = "Queued"
            elif i == 1:
                status = "Starting"
            elif i < 9:
                status = "Running"
            else:
                status = "Success"
            rsps.add(
                rsps.GET,
                f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/",
                json=sample_run_details(status_humanized=status),
            )

        # 404 when trying to access run results
        rsps.add(
            rsps.GET,
            f"{SAMPLE_API_PREFIX}/runs/{SAMPLE_RUN_ID}/artifacts/run_results.json",
            status=404,
        )

        dbt_cloud_output = dc_resource.run_job_and_poll(
            SAMPLE_JOB_ID, poll_interval=0.05, poll_timeout=1
        )

        assert dbt_cloud_output.result == {}  # run_result.json not available
        assert dbt_cloud_output.run_details == sample_run_details()["data"]
