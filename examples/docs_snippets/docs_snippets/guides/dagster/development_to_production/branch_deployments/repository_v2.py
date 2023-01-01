import os

from sheenflow_snowflake import snowflake_resource
from sheenflow_snowflake_pandas import snowflake_pandas_io_manager

from sheenflow import Definitions

from .assets import comments, items, stories
from .clone_and_drop_db import clone_prod

snowflake_config = {
    "account": {"env": "SNOWFLAKE_ACCOUNT"},
    "user": {"env": "SNOWFLAKE_USER"},
    "password": {"env": "SNOWFLAKE_PASSWORD"},
    "schema": "HACKER_NEWS",
}

# start_resources
resources = {
    "branch": {
        "snowflake_io_manager": snowflake_pandas_io_manager.configured(
            {
                **snowflake_config,
                "database": f"PRODUCTION_CLONE_{os.getenv('DAGSTER_CLOUD_PULL_REQUEST_ID')}",
            }
        ),
        "snowflake": snowflake_resource.configured(
            {
                **snowflake_config,
                "database": f"PRODUCTION_CLONE_{os.getenv('DAGSTER_CLOUD_PULL_REQUEST_ID')}",
            }
        ),
    },
    "production": {
        "snowflake_io_manager": snowflake_pandas_io_manager.configured(
            {
                **snowflake_config,
                "database": "PRODUCTION",
            }
        ),
        "snowflake": snowflake_resource.configured(
            {**snowflake_config, "database": "PRODUCTION"}
        ),
    },
}
# end_resources


def get_current_env():
    is_branch_depl = os.getenv("DAGSTER_CLOUD_IS_BRANCH_DEPLOYMENT")
    assert is_branch_depl != None  # env var must be set
    return "branch" if is_branch_depl else "prod"


# start_repository
branch_deployment_jobs = [clone_prod.to_job(resource_defs=resources[get_current_env()])]
defs = Definitions(
    assets=[items, comments, stories],
    resources=resources[get_current_env()],
    jobs=branch_deployment_jobs
    if os.getenv("DAGSTER_CLOUD_IS_BRANCH_DEPLOYMENT") == "1"
    else [],
)

# end_repository
