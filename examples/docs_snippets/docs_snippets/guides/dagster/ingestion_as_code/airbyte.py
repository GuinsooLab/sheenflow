# isort: skip_file
# pylint: disable=unused-variable


def scope_define_reconciler():
    # start_define_reconciler
    from sheenflow_airbyte import AirbyteManagedElementReconciler, airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
            # If using basic auth, include username and password:
            "username": "airbyte",
            "password": {"env": "AIRBYTE_PASSWORD"},
        }
    )

    airbyte_reconciler = AirbyteManagedElementReconciler(
        airbyte=airbyte_instance,
        connections=[],
    )
    # end_define_reconciler

    # start_define_sources
    from sheenflow_airbyte.managed.generated.sources import FileSource
    from sheenflow_airbyte.managed.generated.destinations import LocalJsonDestination

    cereals_csv_source = FileSource(
        name="cereals-csv",
        url="https://docs.dagster.io/assets/cereal.csv",
        format="csv",
        provider=FileSource.HTTPSPublicWeb(),
        dataset_name="cereals",
    )

    local_json_destination = LocalJsonDestination(
        name="local-json",
        destination_path="/local/cereals_out.json",
    )
    # end_define_sources

    # start_define_connection
    from sheenflow_airbyte import AirbyteConnection, AirbyteSyncMode

    cereals_connection = AirbyteConnection(
        name="download-cereals",
        source=cereals_csv_source,
        destination=local_json_destination,
        stream_config={"cereals": AirbyteSyncMode.full_refresh_overwrite()},
    )
    # end_define_connection

    # start_new_reconciler
    airbyte_reconciler = AirbyteManagedElementReconciler(
        airbyte=airbyte_instance,
        connections=[cereals_connection],
    )
    # end_new_reconciler

    # start_new_reconciler_delete
    airbyte_reconciler = AirbyteManagedElementReconciler(
        airbyte=airbyte_instance, connections=[...], delete_unmentioned_resources=True
    )
    # end_new_reconciler_delete

    # start_load_assets
    from sheenflow_airbyte import load_assets_from_connections, airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": 8000,
            # If using basic auth, include username and password:
            "username": "airbyte",
            "password": {"env": "AIRBYTE_PASSWORD"},
        }
    )

    airbyte_assets = load_assets_from_connections(
        airbyte=airbyte_instance, connections=[cereals_connection]
    )
    # end_load_assets
