import os

from dagster_snowflake_pandas import snowflake_pandas_io_manager
from development_to_production.assets import comments, items, stories

from dagster import Definitions

# start
# __init__.py


resources = {
    "local": {
        "snowflake_io_manager": snowflake_pandas_io_manager.configured(
            {
                "account": "abc1234.us-east-1",
                "user": {"env": "DEV_SNOWFLAKE_USER"},
                "password": {"env": "DEV_SNOWFLAKE_PASSWORD"},
                "database": "LOCAL",
                "schema": {"env": "DEV_SNOWFLAKE_SCHEMA"},
            }
        ),
    },
    "production": {
        "snowflake_io_manager": snowflake_pandas_io_manager.configured(
            {
                "account": "abc1234.us-east-1",
                "user": "system@company.com",
                "password": {"env": "SYSTEM_SNOWFLAKE_PASSWORD"},
                "database": "PRODUCTION",
                "schema": "HACKER_NEWS",
            }
        ),
    },
}
deployment_name = os.getenv("DAGSTER_DEPLOYMENT", "local")

defs = Definitions(
    assets=[items, comments, stories], resources=resources[deployment_name]
)

# end


# start_staging

resources = {
    "local": {...},
    "production": {...},
    "staging": {
        "snowflake_io_manager": snowflake_pandas_io_manager.configured(
            {
                "account": "abc1234.us-east-1",
                "user": "system@company.com",
                "password": {"env": "SYSTEM_SNOWFLAKE_PASSWORD"},
                "database": "STAGING",
                "schema": "HACKER_NEWS",
            }
        ),
    },
}

# end_staging

from ..resources.resources_v1 import HNAPIClient

# start_hn_resource

resource_defs = {
    "local": {"hn_client": HNAPIClient(), "snowflake_io_manager": {...}},
    "production": {"hn_client": HNAPIClient(), "snowflake_io_manager": {...}},
    "staging": {"hn_client": HNAPIClient(), "snowflake_io_manager": {...}},
}

# end_hn_resource