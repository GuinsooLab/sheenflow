# isort: skip_file
# pylint: disable=unused-variable


def scope_define_instance():
    # start_define_instance
    from sheenflow_fivetran import fivetran_resource

    # Pull API key and secret from environment variables
    fivetran_instance = fivetran_resource.configured(
        {
            "api_key": {"env": "FIVETRAN_API_KEY"},
            "api_secret": {"env": "FIVETRAN_API_SECRET"},
        }
    )
    # end_define_instance


def scope_load_assets_from_fivetran_instance():
    from sheenflow_fivetran import fivetran_resource

    fivetran_instance = fivetran_resource.configured(
        {
            "api_key": {"env": "FIVETRAN_API_KEY"},
            "api_secret": {"env": "FIVETRAN_API_SECRET"},
        }
    )
    # start_load_assets_from_fivetran_instance
    from sheenflow_fivetran import load_assets_from_fivetran_instance

    # Use the fivetran_instance resource we defined in Step 1
    fivetran_assets = load_assets_from_fivetran_instance(fivetran_instance)
    # end_load_assets_from_fivetran_instance


def scope_manually_define_fivetran_assets():
    # start_manually_define_fivetran_assets
    from sheenflow_fivetran import build_fivetran_assets

    fivetran_assets = build_fivetran_assets(
        connector_id="omit_constitutional",
        destination_tables=["public.survey_responses", "public.surveys"],
    )
    # end_manually_define_fivetran_assets


def scope_fivetran_manual_config():
    from sheenflow_fivetran import fivetran_resource

    fivetran_instance = fivetran_resource.configured(
        {
            "api_key": {"env": "FIVETRAN_API_KEY"},
            "api_secret": {"env": "FIVETRAN_API_SECRET"},
        }
    )
    # start_fivetran_manual_config
    from sheenflow_fivetran import build_fivetran_assets

    from sheenflow import with_resources

    fivetran_assets = with_resources(
        build_fivetran_assets(
            connector_id="omit_constitutional",
            destination_tables=["public.survey_responses", "public.surveys"],
        ),
        # Use the fivetran_instance resource we defined in Step 1
        {"fivetran": fivetran_instance},
    )
    # end_fivetran_manual_config


def scope_schedule_assets():
    from sheenflow_fivetran import fivetran_resource, load_assets_from_fivetran_instance

    fivetran_instance = fivetran_resource.configured(
        {"api_key": "foo", "api_secret": "bar"}
    )
    fivetran_assets = load_assets_from_fivetran_instance(fivetran_instance)

    # start_schedule_assets
    from sheenflow import (
        ScheduleDefinition,
        define_asset_job,
        AssetSelection,
        Definitions,
    )

    # materialize all assets
    run_everything_job = define_asset_job("run_everything", selection="*")

    # only run my_fivetran_connection and downstream assets
    my_etl_job = define_asset_job(
        "my_etl_job", AssetSelection.groups("my_fivetran_connection").downstream()
    )

    defs = Definitions(
        assets=[fivetran_assets],
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


def scope_add_downstream_assets():
    from sheenflow_fivetran import fivetran_resource

    fivetran_instance = fivetran_resource.configured(
        {
            "api_key": {"env": "FIVETRAN_API_KEY"},
            "api_secret": {"env": "FIVETRAN_API_SECRET"},
        }
    )
    snowflake_io_manager = ...

    # start_add_downstream_assets
    import json
    from sheenflow import asset, AssetIn, AssetKey, Definitions
    from sheenflow_fivetran import load_assets_from_fivetran_instance

    fivetran_assets = load_assets_from_fivetran_instance(
        fivetran_instance,
        io_manager_key="snowflake_io_manager",
    )

    @asset(
        ins={"survey_responses": AssetIn(key=AssetKey(["public", "survey_responses"]))}
    )
    def survey_responses_file(survey_responses):
        with open("survey_responses.json", "w", encoding="utf8") as f:
            f.write(json.dumps(survey_responses, indent=2))

    defs = Definitions(
        assets=[fivetran_assets, survey_responses_file],
        resources={"snowflake_io_manager": snowflake_io_manager},
    )
    # end_add_downstream_assets
