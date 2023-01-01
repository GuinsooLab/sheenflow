# isort: skip_file
# pylint: disable=unused-variable


def scope_define_instance():
    # start_define_dbt_cloud_instance
    from sheenflow_dbt import dbt_cloud_resource

    dbt_cloud_instance = dbt_cloud_resource.configured(
        {
            "auth_token": {"env": "DBT_CLOUD_API_TOKEN"},
            "account_id": {"env": "DBT_CLOUD_ACCOUNT_ID"},
        }
    )
    # end_define_dbt_cloud_instance


def scope_load_assets_from_dbt_cloud_job():
    from sheenflow_dbt import dbt_cloud_resource

    dbt_cloud_instance = dbt_cloud_resource.configured(
        {
            "auth_token": {"env": "DBT_CLOUD_API_TOKEN"},
            "account_id": {"env": "DBT_CLOUD_ACCOUNT_ID"},
        }
    )
    # start_load_assets_from_dbt_cloud_job
    from sheenflow_dbt import load_assets_from_dbt_cloud_job

    # Use the dbt_cloud_instance resource we defined in Step 1, and the job_id from Prerequisites
    dbt_cloud_assets = load_assets_from_dbt_cloud_job(
        dbt_cloud=dbt_cloud_instance,
        job_id=33333,
    )
    # end_load_assets_from_dbt_cloud_job


def scope_schedule_dbt_cloud_assets(dbt_cloud_assets):
    # start_schedule_dbt_cloud_assets
    from sheenflow import (
        ScheduleDefinition,
        define_asset_job,
        AssetSelection,
        Definitions,
    )

    # Materialize all assets
    run_everything_job = define_asset_job("run_everything_job", AssetSelection.all())

    # Materialize only the staging assets
    run_staging_job = define_asset_job(
        "run_staging_job", AssetSelection.groups("staging")
    )

    defs = Definitions(
        # Use the dbt_cloud_assets defined in Step 2
        assets=[dbt_cloud_assets],
        schedules=[
            ScheduleDefinition(
                job=run_everything_job,
                cron_schedule="@daily",
            ),
            ScheduleDefinition(
                job=run_staging_job,
                cron_schedule="@hourly",
            ),
        ],
    )

    # end_schedule_dbt_cloud_assets
