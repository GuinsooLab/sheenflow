import json
from copy import deepcopy
from typing import List, Optional

import pytest
import responses
from sheenflow_dbt import (
    DagsterDbtCloudJobInvariantViolationError,
    dbt_cloud_resource,
    load_assets_from_dbt_cloud_job,
)

from sheenflow import (
    AssetKey,
    AssetSelection,
    DailyPartitionsDefinition,
    FreshnessPolicy,
    MetadataValue,
    asset,
    build_init_resource_context,
    define_asset_job,
    file_relative_path,
)
from sheenflow._core.test_utils import instance_for_test

from ..utils import assert_assets_match_project

DBT_CLOUD_API_TOKEN = "abc"
DBT_CLOUD_ACCOUNT_ID = 1
DBT_CLOUD_PROJECT_ID = 12
DBT_CLOUD_JOB_ID = 123
DBT_CLOUD_RUN_ID = 1234

with open(file_relative_path(__file__, "../sample_manifest.json"), "r", encoding="utf8") as f:
    MANIFEST_JSON = json.load(f)

with open(file_relative_path(__file__, "../sample_run_results.json"), "r", encoding="utf8") as f:
    RUN_RESULTS_JSON = json.load(f)


@pytest.fixture(name="dbt_cloud")
def dbt_cloud_fixture():
    yield dbt_cloud_resource.configured(
        {
            "auth_token": DBT_CLOUD_API_TOKEN,
            "account_id": DBT_CLOUD_ACCOUNT_ID,
        }
    )


@pytest.fixture(name="dbt_cloud_service")
def dbt_cloud_service_fixture():
    yield dbt_cloud_resource(
        build_init_resource_context(
            config={
                "auth_token": DBT_CLOUD_API_TOKEN,
                "account_id": DBT_CLOUD_ACCOUNT_ID,
            }
        )
    )


def _add_dbt_cloud_job_responses(
    dbt_cloud_api_base_url: str, dbt_commands: List[str], run_results_json: Optional[dict] = None
):
    run_results_json = run_results_json or RUN_RESULTS_JSON

    responses.add(
        method=responses.GET,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/jobs/{DBT_CLOUD_JOB_ID}/",
        json={
            "data": {
                "project_id": DBT_CLOUD_PROJECT_ID,
                "generate_docs": True,
                "execute_steps": dbt_commands,
                "name": "A dbt Cloud job",
                "id": DBT_CLOUD_JOB_ID,
            }
        },
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/jobs/{DBT_CLOUD_JOB_ID}/",
        json={"data": {}},
        status=200,
    )
    responses.add(
        method=responses.GET,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/runs/",
        json={"data": [{"id": DBT_CLOUD_RUN_ID}]},
        status=200,
    )
    responses.add(
        method=responses.GET,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/runs/{DBT_CLOUD_RUN_ID}/artifacts/manifest.json",
        json=MANIFEST_JSON,
        status=200,
    )
    responses.add(
        method=responses.GET,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/runs/{DBT_CLOUD_RUN_ID}/artifacts/run_results.json",
        json=run_results_json,
        status=200,
    )
    responses.add(
        method=responses.POST,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/jobs/{DBT_CLOUD_JOB_ID}/run/",
        json={"data": {"id": DBT_CLOUD_RUN_ID, "href": "/"}},
        status=200,
    )
    responses.add(
        method=responses.GET,
        url=f"{dbt_cloud_api_base_url}{DBT_CLOUD_ACCOUNT_ID}/runs/{DBT_CLOUD_RUN_ID}/",
        json={"data": {"status_humanized": "Success", "job": {}, "id": DBT_CLOUD_RUN_ID}},
        status=200,
    )


@responses.activate
@pytest.mark.parametrize("before_dbt_materialization_command", [[], ["dbt test"]])
@pytest.mark.parametrize("dbt_materialization_command", ["dbt run", "dbt build"])
@pytest.mark.parametrize(
    "after_dbt_materialization_command",
    [[], ["dbt run-operation upload_dbt_artifacts --args '{filenames: [manifest, run_results]}'"]],
)
@pytest.mark.parametrize(
    ["dbt_materialization_command_options", "expected_dbt_materialization_command_options"],
    [
        ("-s a:b c:d *x", "--select a:b c:d *x"),
        ("--exclude e:f g:h", "--exclude e:f g:h"),
        ("--selector x:y", "--selector x:y"),
        (
            "-s a:b c:d --exclude e:f g:h --selector x:y",
            "--select a:b c:d --exclude e:f g:h --selector x:y",
        ),
    ],
)
def test_load_assets_from_dbt_cloud_job(
    mocker,
    before_dbt_materialization_command,
    dbt_materialization_command,
    after_dbt_materialization_command,
    dbt_materialization_command_options,
    expected_dbt_materialization_command_options,
    dbt_cloud,
    dbt_cloud_service,
):
    dbt_commands = (
        before_dbt_materialization_command
        + [f"{dbt_materialization_command} {dbt_materialization_command_options}"]
        + after_dbt_materialization_command
    )
    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=dbt_commands,
    )

    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud, job_id=DBT_CLOUD_JOB_ID
    )

    mock_run_job_and_poll = mocker.patch(
        "sheenflow_dbt.cloud.resources.DbtCloudResourceV2.run_job_and_poll",
        wraps=dbt_cloud_cacheable_assets._dbt_cloud.run_job_and_poll,  # pylint: disable=protected-access
    )

    dbt_assets_definition_cacheable_data = dbt_cloud_cacheable_assets.compute_cacheable_data()
    dbt_cloud_assets = dbt_cloud_cacheable_assets.build_definitions(
        dbt_assets_definition_cacheable_data
    )

    mock_run_job_and_poll.assert_called_once_with(
        job_id=DBT_CLOUD_JOB_ID,
        cause="Generating software-defined assets for Dagster.",
        steps_override=[f"dbt compile {expected_dbt_materialization_command_options}"],
    )

    assert_assets_match_project(dbt_cloud_assets, has_non_argument_deps=True)

    mock_run_job_and_poll.reset_mock()

    # Assert that the outputs have the correct metadata
    for output in dbt_cloud_assets[0].op.output_dict.values():
        assert output.metadata.keys() == {"dbt Cloud Job", "dbt Cloud Documentation"}
        assert output.metadata["dbt Cloud Job"] == MetadataValue.url(
            dbt_cloud_service.build_url_for_job(
                project_id=DBT_CLOUD_PROJECT_ID, job_id=DBT_CLOUD_JOB_ID
            )
        )

    materialize_cereal_assets = define_asset_job(
        name="materialize_cereal_assets",
        selection=AssetSelection.assets(*dbt_cloud_assets),
    ).resolve(assets=dbt_cloud_assets, source_assets=[])

    with instance_for_test() as instance:
        result = materialize_cereal_assets.execute_in_process(instance=instance)

    assert result.success

    mock_run_job_and_poll.assert_called_once_with(
        job_id=DBT_CLOUD_JOB_ID,
        cause=f"Materializing software-defined assets in Dagster run {result.run_id[:8]}",
        steps_override=dbt_commands,
    )


@responses.activate
@pytest.mark.parametrize(
    "invalid_dbt_commands",
    [
        [],
        ["dbt deps"],
        ["dbt deps", "dbt test"],
        [f"dbt build --vars '{json.dumps({'static_variable': 'bad'})}'"],
    ],
    ids=[
        "empty commands",
        "no run/build step",
        "multiple commands, no run/build step",
        "has static variables",
    ],
)
def test_invalid_dbt_cloud_job_commands(dbt_cloud, dbt_cloud_service, invalid_dbt_commands):
    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud, job_id=DBT_CLOUD_JOB_ID
    )

    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=invalid_dbt_commands,
    )

    with pytest.raises(DagsterDbtCloudJobInvariantViolationError):
        dbt_cloud_cacheable_assets.compute_cacheable_data()


@responses.activate
def test_empty_assets_dbt_cloud_job(dbt_cloud, dbt_cloud_service):
    empty_run_results_json = deepcopy(RUN_RESULTS_JSON)
    empty_run_results_json["results"] = []
    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud, job_id=DBT_CLOUD_JOB_ID
    )

    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=["dbt build"],
        run_results_json=empty_run_results_json,
    )

    with pytest.raises(DagsterDbtCloudJobInvariantViolationError):
        dbt_cloud_cacheable_assets.compute_cacheable_data()


@responses.activate
def test_custom_groups(dbt_cloud, dbt_cloud_service):
    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=["dbt build"],
    )

    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud,
        job_id=DBT_CLOUD_JOB_ID,
        node_info_to_group_fn=lambda node_info: node_info["tags"][0],
    )
    dbt_assets_definition_cacheable_data = dbt_cloud_cacheable_assets.compute_cacheable_data()
    dbt_cloud_assets = dbt_cloud_cacheable_assets.build_definitions(
        dbt_assets_definition_cacheable_data
    )

    assert dbt_cloud_assets[0].group_names_by_key == {
        AssetKey(["cold_schema", "sort_cold_cereals_by_calories"]): "foo",
        AssetKey(["sort_by_calories"]): "foo",
        AssetKey(["sort_hot_cereals_by_calories"]): "bar",
        AssetKey(["subdir_schema", "least_caloric"]): "bar",
    }


@responses.activate
def test_node_info_to_asset_key(dbt_cloud, dbt_cloud_service):
    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=["dbt build"],
    )

    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud,
        job_id=DBT_CLOUD_JOB_ID,
        node_info_to_asset_key=lambda node_info: AssetKey(["foo", node_info["name"]]),
    )
    dbt_assets_definition_cacheable_data = dbt_cloud_cacheable_assets.compute_cacheable_data()
    dbt_cloud_assets = dbt_cloud_cacheable_assets.build_definitions(
        dbt_assets_definition_cacheable_data
    )

    assert dbt_cloud_assets[0].group_names_by_key.keys() == {
        AssetKey(["foo", "sort_cold_cereals_by_calories"]),
        AssetKey(["foo", "sort_by_calories"]),
        AssetKey(["foo", "sort_hot_cereals_by_calories"]),
        AssetKey(["foo", "least_caloric"]),
    }


@responses.activate
def test_custom_freshness_policy(dbt_cloud, dbt_cloud_service):
    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=["dbt build"],
    )

    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud,
        job_id=DBT_CLOUD_JOB_ID,
        node_info_to_freshness_policy_fn=lambda node_info: FreshnessPolicy(
            maximum_lag_minutes=len(node_info["name"])
        ),
    )
    dbt_assets_definition_cacheable_data = dbt_cloud_cacheable_assets.compute_cacheable_data()
    dbt_cloud_assets = dbt_cloud_cacheable_assets.build_definitions(
        dbt_assets_definition_cacheable_data
    )

    assert dbt_cloud_assets[0].freshness_policies_by_key == {
        key: FreshnessPolicy(maximum_lag_minutes=len(key.path[-1]))
        for key in dbt_cloud_assets[0].keys
    }


@responses.activate
def test_partitions(mocker, dbt_cloud, dbt_cloud_service):
    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=["dbt build"],
    )

    partition_def = DailyPartitionsDefinition(start_date="2022-01-01")
    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud,
        job_id=DBT_CLOUD_JOB_ID,
        partitions_def=partition_def,
        partition_key_to_vars_fn=lambda partition_key: {"run_date": partition_key},
        # FreshnessPolicies not currently supported for partitioned assets
        node_info_to_freshness_policy_fn=lambda _: None,
    )

    mock_run_job_and_poll = mocker.patch(
        "sheenflow_dbt.cloud.resources.DbtCloudResourceV2.run_job_and_poll",
        wraps=dbt_cloud_cacheable_assets._dbt_cloud.run_job_and_poll,  # pylint: disable=protected-access
    )

    dbt_assets_definition_cacheable_data = dbt_cloud_cacheable_assets.compute_cacheable_data()
    dbt_cloud_assets = dbt_cloud_cacheable_assets.build_definitions(
        dbt_assets_definition_cacheable_data
    )

    mock_run_job_and_poll.assert_called_once_with(
        job_id=DBT_CLOUD_JOB_ID,
        cause="Generating software-defined assets for Dagster.",
        steps_override=[
            f"dbt compile --vars '{json.dumps({'run_date': partition_def.get_last_partition_key()})}'"
        ],
    )

    mock_run_job_and_poll.reset_mock()

    materialize_cereal_assets = define_asset_job(
        name="materialize_partitioned_cereal_assets",
        selection=AssetSelection.assets(*dbt_cloud_assets),
    ).resolve(assets=dbt_cloud_assets, source_assets=[])

    with instance_for_test() as instance:
        result = materialize_cereal_assets.execute_in_process(
            instance=instance,
            partition_key="2022-02-01",
        )

    assert result.success

    mock_run_job_and_poll.assert_called_once_with(
        job_id=DBT_CLOUD_JOB_ID,
        cause=f"Materializing software-defined assets in Dagster run {result.run_id[:8]}",
        steps_override=[f"dbt build --vars '{json.dumps({'run_date': '2022-02-01'})}'"],
    )


@responses.activate
@pytest.mark.parametrize(
    "asset_selection, expected_dbt_asset_names",
    [
        (
            "*",
            "",  # All dbt assets are chosen, so no selection is made
        ),
        (
            "sort_by_calories+",
            "",  # All dbt assets are chosen, so no selection is made
        ),
        (
            "*hanger2",
            "dagster_dbt_test_project.sort_by_calories,dagster_dbt_test_project.subdir.least_caloric",
        ),
        (
            [
                "cold_schema/sort_cold_cereals_by_calories",
                "subdir_schema/least_caloric",
            ],
            "dagster_dbt_test_project.sort_cold_cereals_by_calories,dagster_dbt_test_project.subdir.least_caloric",
        ),
    ],
)
def test_subsetting(
    mocker, dbt_cloud, dbt_cloud_service, asset_selection, expected_dbt_asset_names
):
    _add_dbt_cloud_job_responses(
        dbt_cloud_api_base_url=dbt_cloud_service.api_base_url,
        dbt_commands=["dbt build"],
    )

    dbt_cloud_cacheable_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud,
        job_id=DBT_CLOUD_JOB_ID,
    )

    mock_run_job_and_poll = mocker.patch(
        "sheenflow_dbt.cloud.resources.DbtCloudResourceV2.run_job_and_poll",
        wraps=dbt_cloud_cacheable_assets._dbt_cloud.run_job_and_poll,  # pylint: disable=protected-access
    )

    dbt_assets_definition_cacheable_data = dbt_cloud_cacheable_assets.compute_cacheable_data()
    dbt_cloud_assets = dbt_cloud_cacheable_assets.build_definitions(
        dbt_assets_definition_cacheable_data
    )

    mock_run_job_and_poll.reset_mock()

    @asset(non_argument_deps={AssetKey("sort_by_calories")})
    def hanger1():
        return None

    @asset(non_argument_deps={AssetKey(["subdir_schema", "least_caloric"])})
    def hanger2():
        return None

    materialize_cereal_assets = define_asset_job(
        name="materialize_cereal_assets",
        selection=asset_selection,
    ).resolve(assets=list(dbt_cloud_assets) + [hanger1, hanger2], source_assets=[])

    with instance_for_test() as instance:
        result = materialize_cereal_assets.execute_in_process(instance=instance)

    assert result.success

    expected_dbt_asset_names = (
        expected_dbt_asset_names.split(",") if expected_dbt_asset_names else []
    )
    dbt_filter_option = (
        f"--select {' '.join(expected_dbt_asset_names)}" if expected_dbt_asset_names else ""
    )
    mock_run_job_and_poll.assert_called_once_with(
        job_id=DBT_CLOUD_JOB_ID,
        cause=f"Materializing software-defined assets in Dagster run {result.run_id[:8]}",
        steps_override=[f"dbt build {dbt_filter_option}".strip()],
    )
