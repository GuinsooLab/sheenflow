plot_data = None

# start_example

import pandas as pd
from sheenflow_aws.s3.io_manager import s3_pickle_io_manager
from sheenflow_snowflake_pandas import snowflake_pandas_io_manager

from sheenflow import Definitions, asset


@asset(io_manager_key="warehouse_io_manager")
def iris_dataset() -> pd.DataFrame:
    return pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
        names=[
            "Sepal length (cm)",
            "Sepal width (cm)",
            "Petal length (cm)",
            "Petal width (cm)",
            "Species",
        ],
    )


@asset(io_manager_key="blob_io_manager")
def iris_plots(iris_dataset):
    # plot_data is a function we've defined somewhere else
    # that plots the data in a DataFrame
    return plot_data(iris_dataset)


defs = Definitions(
    assets=[iris_dataset, iris_plots],
    resources={
        "warehouse_io_manager": snowflake_pandas_io_manager.configured(
            {
                "database": "FLOWERS",
                "schema": "IRIS",
                "account": "abc1234.us-east-1",
                "user": {"env": "SNOWFLAKE_USER"},
                "password": {"env": "SNOWFLAKE_PASSWORD"},
            }
        ),
        "blob_io_manager": s3_pickle_io_manager,
    },
)

# end_example
