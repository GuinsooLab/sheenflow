import re

import pytest
import responses
from sheenflow_airbyte import AirbyteOutput, AirbyteState, airbyte_resource
from sheenflow_airbyte.utils import generate_materializations

from sheenflow import DagsterExecutionInterruptedError, Failure, MetadataEntry
from sheenflow import _check as check
from sheenflow import build_init_resource_context

from .utils import get_sample_connection_json, get_sample_job_json, get_sample_job_list_json


@responses.activate
def test_trigger_connection():
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json={"job": {"id": 1}},
        status=200,
    )
    resp = ab_resource.start_sync("some_connection")
    assert resp == {"job": {"id": 1}}


def test_trigger_connection_fail():
    ab_resource = airbyte_resource(
        build_init_resource_context(config={"host": "some_host", "port": "8000"})
    )
    with pytest.raises(
        Failure,
        match=re.escape(
            "Max retries (3) exceeded with url: http://some_host:8000/api/v1/connections/get."
        ),
    ):
        ab_resource.sync_and_poll("some_connection")


@responses.activate
@pytest.mark.parametrize(
    "state",
    [AirbyteState.SUCCEEDED, AirbyteState.CANCELLED, AirbyteState.ERROR, "unrecognized"],
)
@pytest.mark.parametrize(
    "forward_logs",
    [True, False],
)
def test_sync_and_poll(state, forward_logs):
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
                "forward_logs": forward_logs,
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json=get_sample_connection_json(),
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json={"job": {"id": 1}},
        status=200,
    )
    if forward_logs:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            json={"job": {"id": 1, "status": state}},
            status=200,
        )
    else:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json={"jobs": [{"job": {"id": 1, "status": state}}]},
            status=200,
        )

    if state == "unrecognized":
        responses.add(responses.POST, f"{ab_resource.api_base_url}/jobs/cancel", status=204)

    if state == AirbyteState.ERROR:
        with pytest.raises(Failure, match="Job failed"):
            ab_resource.sync_and_poll("some_connection", 0)

    elif state == AirbyteState.CANCELLED:
        with pytest.raises(Failure, match="Job was cancelled"):
            ab_resource.sync_and_poll("some_connection", 0)

    elif state == "unrecognized":
        with pytest.raises(Failure, match="unexpected state"):
            ab_resource.sync_and_poll("some_connection", 0)

    else:
        result = ab_resource.sync_and_poll("some_connection", 0)
        assert result == AirbyteOutput(
            job_details={"job": {"id": 1, "status": state}},
            connection_details=get_sample_connection_json(),
        )


@responses.activate
def test_start_sync_bad_out_fail():
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json=None,
        status=204,
    )
    with pytest.raises(check.CheckError):
        ab_resource.start_sync("some_connection")


@responses.activate
def test_get_connection_details_bad_out_fail():
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json=None,
        status=204,
    )
    with pytest.raises(check.CheckError):
        ab_resource.get_connection_details("some_connection")


@responses.activate
@pytest.mark.parametrize(
    "forward_logs",
    [True, False],
)
def test_get_job_status_bad_out_fail(forward_logs):
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    if forward_logs:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            json=None,
            status=204,
        )
        with pytest.raises(check.CheckError):
            ab_resource.get_job_status("some_connection", 5)
    else:
        # Test no-forward-logs config
        ab_resource = airbyte_resource(
            build_init_resource_context(
                config={
                    "host": "some_host",
                    "port": "8000",
                    "forward_logs": False,
                }
            )
        )
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json=None,
            status=204,
        )
        with pytest.raises(check.CheckError):
            ab_resource.get_job_status("some_connection", 5)

        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json={"jobs": []},
            status=200,
        )
        with pytest.raises(check.CheckError):
            ab_resource.get_job_status("some_connection", 5)


@responses.activate
def test_logging_multi_attempts(capsys):
    def _get_attempt(ls):
        return {"logs": {"logLines": ls}}

    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json={},
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json={"job": {"id": 1}},
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/jobs/get",
        json={"job": {"id": 1, "status": "pending"}},
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/jobs/get",
        json={
            "job": {"id": 1, "status": "running"},
            "attempts": [_get_attempt(ls) for ls in [["log1a"]]],
        },
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/jobs/get",
        json={
            "job": {"id": 1, "status": "running"},
            "attempts": [_get_attempt(ls) for ls in [["log1a", "log1b"]]],
        },
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/jobs/get",
        json={
            "job": {"id": 1, "status": "running"},
            "attempts": [
                _get_attempt(ls) for ls in [["log1a", "log1b", "log1c"], ["log2a", "log2b"]]
            ],
        },
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/jobs/get",
        json={
            "job": {"id": 1, "status": AirbyteState.SUCCEEDED},
            "attempts": [
                _get_attempt(ls) for ls in [["log1a", "log1b", "log1c"], ["log2a", "log2b"]]
            ],
        },
        status=200,
    )
    responses.add(responses.POST, f"{ab_resource.api_base_url}/jobs/cancel", status=204)
    ab_resource.sync_and_poll("some_connection", 0, None)
    captured = capsys.readouterr()
    assert captured.out == "\n".join(["log1a", "log1b", "log1c", "log2a", "log2b"]) + "\n"


@responses.activate
@pytest.mark.parametrize(
    "forward_logs",
    [True, False],
)
def test_assets(forward_logs):

    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
                "forward_logs": forward_logs,
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json=get_sample_connection_json(),
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json={"job": {"id": 1}},
        status=200,
    )

    if forward_logs:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            json=get_sample_job_json(),
            status=200,
        )
    else:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json=get_sample_job_list_json(),
            status=200,
        )
    responses.add(responses.POST, f"{ab_resource.api_base_url}/jobs/cancel", status=204)

    airbyte_output = ab_resource.sync_and_poll("some_connection", 0, None)

    materializations = list(generate_materializations(airbyte_output, []))
    assert len(materializations) == 3

    assert MetadataEntry("bytesEmitted", value=1234) in materializations[0].metadata_entries
    assert MetadataEntry("recordsCommitted", value=4321) in materializations[0].metadata_entries


@responses.activate
@pytest.mark.parametrize(
    "forward_logs,cancel_sync_on_run_termination",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_sync_and_poll_termination(forward_logs, cancel_sync_on_run_termination):
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
                "forward_logs": forward_logs,
                "cancel_sync_on_run_termination": cancel_sync_on_run_termination,
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json={},
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json={"job": {"id": 1}},
        status=200,
    )

    # Simulate job interruption when we poll for job status
    def callback(*_, **__):
        raise DagsterExecutionInterruptedError()

    if forward_logs:
        responses.add_callback(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            callback=callback,
        )
    else:
        responses.add_callback(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            callback=callback,
        )
    responses.add(responses.POST, f"{ab_resource.api_base_url}/jobs/cancel", status=204)
    poll_wait_second = 2
    timeout = 1
    with pytest.raises(DagsterExecutionInterruptedError):
        ab_resource.sync_and_poll("some_connection", poll_wait_second, timeout)
        if cancel_sync_on_run_termination:
            assert responses.assert_call_count(f"{ab_resource.api_base_url}/jobs/cancel", 1) is True
        else:
            assert responses.assert_call_count(f"{ab_resource.api_base_url}/jobs/cancel", 0) is True


@responses.activate
@pytest.mark.parametrize(
    "forward_logs,cancel_sync_on_run_termination",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_sync_and_poll_timeout(forward_logs, cancel_sync_on_run_termination):
    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
                "forward_logs": forward_logs,
                "cancel_sync_on_run_termination": cancel_sync_on_run_termination,
            }
        )
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json={},
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/sync",
        json={"job": {"id": 1}},
        status=200,
    )
    if forward_logs:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            json={"job": {"id": 1, "status": "pending"}},
            status=200,
        )
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            json={"job": {"id": 1, "status": "running"}},
            status=200,
        )
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/get",
            json={"job": {"id": 1, "status": "running"}},
            status=200,
        )
    else:
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json={"jobs": [{"job": {"id": 1, "status": "pending"}}]},
            status=200,
        )
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json={"jobs": [{"job": {"id": 1, "status": "running"}}]},
            status=200,
        )
        responses.add(
            method=responses.POST,
            url=ab_resource.api_base_url + "/jobs/list",
            json={"jobs": [{"job": {"id": 1, "status": "running"}}]},
            status=200,
        )
    responses.add(responses.POST, f"{ab_resource.api_base_url}/jobs/cancel", status=204)
    poll_wait_second = 2
    timeout = 1
    with pytest.raises(Failure, match="Timeout: Airbyte job"):
        ab_resource.sync_and_poll("some_connection", poll_wait_second, timeout)
        if cancel_sync_on_run_termination:
            assert responses.assert_call_count(f"{ab_resource.api_base_url}/jobs/cancel", 1) is True
        else:
            assert responses.assert_call_count(f"{ab_resource.api_base_url}/jobs/cancel", 0) is True
