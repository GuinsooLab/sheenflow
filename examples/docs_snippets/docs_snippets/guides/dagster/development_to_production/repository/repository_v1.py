# start
# __init__.py
from sheenflow_snowflake_pandas import snowflake_pandas_io_manager
from development_to_production.assets import comments, items, stories

from sheenflow import Definitions

# Note that storing passwords in configuration is bad practice. It will be resolved later in the guide.
resources = {
    "snowflake_io_manager": snowflake_pandas_io_manager.configured(
        {
            "account": "abc1234.us-east-1",
            "user": "me@company.com",
            # password in config is bad practice
            "password": "my_super_secret_password",
            "database": "LOCAL",
            "schema": "ALICE",
        }
    ),
}

defs = Definitions(assets=[items, comments, stories], resources=resources)


# end
