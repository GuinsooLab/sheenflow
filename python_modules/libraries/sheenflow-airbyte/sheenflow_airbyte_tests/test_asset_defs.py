import pytest
import responses
from sheenflow_airbyte import airbyte_resource, build_airbyte_assets

from sheenflow import AssetKey, MetadataEntry, TableColumn, TableSchema, build_init_resource_context
from sheenflow._core.definitions.source_asset import SourceAsset
from sheenflow._legacy import build_assets_job

from .utils import get_sample_connection_json, get_sample_job_json


@responses.activate
@pytest.mark.parametrize("schema_prefix", ["", "the_prefix_"])
def test_assets(schema_prefix):

    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    destination_tables = ["foo", "bar"]
    if schema_prefix:
        destination_tables = [schema_prefix + t for t in destination_tables]
    ab_assets = build_airbyte_assets(
        "12345",
        destination_tables=destination_tables,
        asset_key_prefix=["some", "prefix"],
    )

    assert ab_assets[0].keys == {AssetKey(["some", "prefix", t]) for t in destination_tables}
    assert len(ab_assets[0].op.output_defs) == 2

    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json=get_sample_connection_json(prefix=schema_prefix),
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
        json=get_sample_job_json(schema_prefix=schema_prefix),
        status=200,
    )

    ab_job = build_assets_job(
        "ab_job",
        ab_assets,
        resource_defs={
            "airbyte": airbyte_resource.configured(
                {
                    "host": "some_host",
                    "port": "8000",
                }
            )
        },
    )

    res = ab_job.execute_in_process()

    materializations = [
        event.event_specific_data.materialization
        for event in res.events_for_node("airbyte_sync_12345")
        if event.event_type_value == "ASSET_MATERIALIZATION"
    ]
    assert len(materializations) == 3
    assert {m.asset_key for m in materializations} == {
        AssetKey(["some", "prefix", schema_prefix + "foo"]),
        AssetKey(["some", "prefix", schema_prefix + "bar"]),
        AssetKey(["some", "prefix", schema_prefix + "baz"]),
    }
    assert MetadataEntry("bytesEmitted", value=1234) in materializations[0].metadata_entries
    assert MetadataEntry("recordsCommitted", value=4321) in materializations[0].metadata_entries
    assert (
        MetadataEntry(
            "schema",
            value=TableSchema(
                columns=[
                    TableColumn(name="a", type="str"),
                    TableColumn(name="b", type="int"),
                ]
            ),
        )
        in materializations[0].metadata_entries
    )


@responses.activate
@pytest.mark.parametrize("schema_prefix", ["", "the_prefix_"])
@pytest.mark.parametrize("source_asset", [None, "my_source_asset_key"])
def test_assets_with_normalization(schema_prefix, source_asset):

    ab_resource = airbyte_resource(
        build_init_resource_context(
            config={
                "host": "some_host",
                "port": "8000",
            }
        )
    )
    destination_tables = ["foo", "bar"]
    if schema_prefix:
        destination_tables = [schema_prefix + t for t in destination_tables]

    bar_normalization_tables = {schema_prefix + "bar_baz", schema_prefix + "bar_qux"}
    ab_assets = build_airbyte_assets(
        "12345",
        destination_tables=destination_tables,
        normalization_tables={destination_tables[1]: bar_normalization_tables},
        asset_key_prefix=["some", "prefix"],
        upstream_assets={AssetKey(source_asset)} if source_asset else None,
    )

    assert ab_assets[0].keys == {AssetKey(["some", "prefix", t]) for t in destination_tables} | {
        AssetKey(["some", "prefix", t]) for t in bar_normalization_tables
    }
    assert len(ab_assets[0].op.output_defs) == 4

    responses.add(
        method=responses.POST,
        url=ab_resource.api_base_url + "/connections/get",
        json=get_sample_connection_json(prefix=schema_prefix),
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
        json=get_sample_job_json(schema_prefix=schema_prefix),
        status=200,
    )

    ab_job = build_assets_job(
        "ab_job",
        ab_assets,
        source_assets=[SourceAsset(AssetKey(source_asset))] if source_asset else None,
        resource_defs={
            "airbyte": airbyte_resource.configured(
                {
                    "host": "some_host",
                    "port": "8000",
                }
            )
        },
    )

    res = ab_job.execute_in_process()

    materializations = [
        event.event_specific_data.materialization
        for event in res.events_for_node("airbyte_sync_12345")
        if event.event_type_value == "ASSET_MATERIALIZATION"
    ]
    assert len(materializations) == 5
    assert {m.asset_key for m in materializations} == {
        AssetKey(["some", "prefix", schema_prefix + "foo"]),
        AssetKey(["some", "prefix", schema_prefix + "bar"]),
        AssetKey(["some", "prefix", schema_prefix + "baz"]),
        # Normalized materializations are there
        AssetKey(["some", "prefix", schema_prefix + "bar_baz"]),
        AssetKey(["some", "prefix", schema_prefix + "bar_qux"]),
    }
    assert MetadataEntry("bytesEmitted", value=1234) in materializations[0].metadata_entries
    assert MetadataEntry("recordsCommitted", value=4321) in materializations[0].metadata_entries
    assert (
        MetadataEntry(
            "schema",
            value=TableSchema(
                columns=[
                    TableColumn(name="a", type="str"),
                    TableColumn(name="b", type="int"),
                ]
            ),
        )
        in materializations[0].metadata_entries
    )

    # No metadata for normalized materializations, for now
    assert not materializations[3].metadata_entries
