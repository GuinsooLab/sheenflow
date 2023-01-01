# pylint: disable=redefined-outer-name
import os
import tempfile

import pandas
from sheenflow_pyspark import pyspark_resource
from project_fully_featured.partitions import hourly_partitions
from project_fully_featured.resources.parquet_io_manager import local_partitioned_parquet_io_manager
from pyspark.sql import DataFrame as SparkDF

from sheenflow import asset, materialize


def test_io_manager():
    df_value = pandas.DataFrame({"foo": ["bar", "baz"], "quux": [1, 2]})

    @asset(partitions_def=hourly_partitions)
    def pandas_df_asset():
        return df_value

    @asset(partitions_def=hourly_partitions)
    def spark_input_asset(pandas_df_asset: SparkDF):
        assert isinstance(pandas_df_asset, SparkDF)
        assert pandas_df_asset.count() == 2
        assert set(pandas_df_asset.columns) == {"foo", "quux"}
        return pandas_df_asset

    with tempfile.TemporaryDirectory() as temp_dir:
        res = materialize(
            assets=[pandas_df_asset, spark_input_asset],
            resources={
                "pyspark": pyspark_resource,
                "io_manager": local_partitioned_parquet_io_manager.configured(
                    {"base_path": temp_dir}
                ),
            },
            partition_key="2022-01-01-16:00",
        )

        expected_path = os.path.join(
            temp_dir, "pandas_df_asset", "20220101160000_20220101170000.pq"
        )
        assert res.success
        assert os.path.exists(expected_path)
        intermediate_df = pandas.read_parquet(expected_path)
        assert all(intermediate_df == df_value)
