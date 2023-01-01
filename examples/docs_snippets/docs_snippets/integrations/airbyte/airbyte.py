# isort: skip_file
# pylint: disable=unused-variable


def scope_define_instance():
    # start_define_instance
    from sheenflow_airbyte import airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
            # If using basic auth, include username and password:
            "username": "airbyte",
            "password": {"env": "AIRBYTE_PASSWORD"},
        }
    )
    # end_define_instance


def scope_load_assets_from_airbyte_project():
    # start_load_assets_from_airbyte_project
    from sheenflow_airbyte import load_assets_from_airbyte_project

    airbyte_assets = load_assets_from_airbyte_project(
        project_dir="path/to/airbyte/project",
    )
    # end_load_assets_from_airbyte_project


def scope_load_assets_from_airbyte_instance():
    from sheenflow_airbyte import airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
            # If using basic auth, include username and password:
            "username": "airbyte",
            "password": {"env": "AIRBYTE_PASSWORD"},
        }
    )
    # start_load_assets_from_airbyte_instance
    from sheenflow_airbyte import load_assets_from_airbyte_instance

    # Use the airbyte_instance resource we defined in Step 1
    airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)
    # end_load_assets_from_airbyte_instance


def scope_airbyte_project_config():
    from sheenflow_airbyte import airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
        }
    )
    # start_airbyte_project_config
    from sheenflow_airbyte import load_assets_from_airbyte_project

    from sheenflow import with_resources

    # Use the airbyte_instance resource we defined in Step 1
    airbyte_assets = with_resources(
        [load_assets_from_airbyte_project(project_dir="path/to/airbyte/project")],
        {"airbyte": airbyte_instance},
    )
    # end_airbyte_project_config


def scope_manually_define_airbyte_assets():
    # start_manually_define_airbyte_assets
    from sheenflow_airbyte import build_airbyte_assets

    airbyte_assets = build_airbyte_assets(
        connection_id="87b7fe85-a22c-420e-8d74-b30e7ede77df",
        destination_tables=["releases", "tags", "teams"],
    )
    # end_manually_define_airbyte_assets


def scope_airbyte_manual_config():
    from sheenflow_airbyte import airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
        }
    )
    # start_airbyte_manual_config
    from sheenflow_airbyte import build_airbyte_assets

    from sheenflow import with_resources

    airbyte_assets = with_resources(
        build_airbyte_assets(
            connection_id="87b7fe85-a22c-420e-8d74-b30e7ede77df",
            destination_tables=["releases", "tags", "teams"],
        ),
        # Use the airbyte_instance resource we defined in Step 1
        {"airbyte": airbyte_instance},
    )
    # end_airbyte_manual_config


def scope_add_downstream_assets():
    from sheenflow_airbyte import airbyte_resource

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
        }
    )
    snowflake_io_manager = ...

    # start_add_downstream_assets
    import json
    from sheenflow import asset, Definitions
    from sheenflow_airbyte import load_assets_from_airbyte_instance

    airbyte_assets = load_assets_from_airbyte_instance(
        airbyte_instance,
        io_manager_key="snowflake_io_manager",
    )

    @asset
    def stargazers_file(stargazers):
        with open("stargazers.json", "w", encoding="utf8") as f:
            f.write(json.dumps(stargazers, indent=2))

    defs = Definitions(
        assets=[airbyte_assets, stargazers_file],
        resources={"snowflake_io_manager": snowflake_io_manager},
    )

    # end_add_downstream_assets


def scope_schedule_assets():
    from sheenflow_airbyte import airbyte_resource, load_assets_from_airbyte_instance

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
        }
    )
    airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)

    # start_schedule_assets
    from sheenflow import (
        ScheduleDefinition,
        define_asset_job,
        AssetSelection,
        Definitions,
    )

    # materialize all assets
    run_everything_job = define_asset_job("run_everything", selection="*")

    # only run my_airbyte_connection and downstream assets
    my_etl_job = define_asset_job(
        "my_etl_job", AssetSelection.groups("my_airbyte_connection").downstream()
    )

    defs = Definitions(
        assets=[airbyte_assets],
        schedules=[
            ScheduleDefinition(
                job=my_etl_job,
                cron_schedule="@daily",
            ),
            ScheduleDefinition(
                job=run_everything_job,
                cron_schedule="@weekly",
            ),
        ],
    )

    # end_schedule_assets
