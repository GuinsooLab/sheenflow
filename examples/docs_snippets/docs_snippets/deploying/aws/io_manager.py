from sheenflow_aws.s3.io_manager import s3_pickle_io_manager
from sheenflow_aws.s3.resources import s3_resource

from sheenflow import Int, Out, job, op


@op(out=Out(Int))
def my_op():
    return 1


@job(
    resource_defs={
        "io_manager": s3_pickle_io_manager,
        "s3": s3_resource,
    }
)
def my_job():
    my_op()
