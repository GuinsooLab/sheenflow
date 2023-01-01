import sys

from sheenflow_dask import dask_executor

from sheenflow import job
from sheenflow._utils import file_relative_path

sys.path.append(file_relative_path(__file__, "../../../sheenflow-test/sheenflow_test/toys"))
from hammer import hammer  # pylint: disable=import-error


@job(executor_def=dask_executor)
def hammer_job():
    hammer()
