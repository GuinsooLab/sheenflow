# isort: skip_file
# pylint: disable=reimported

from sheenflow import Definitions

# start_builtin_logger_marker_0
# demo_logger.py

from sheenflow import job, op


@op
def hello_logs(context):
    context.log.info("Hello, world!")


@job
def demo_job():
    hello_logs()


# end_builtin_logger_marker_0


# start_builtin_logger_error_marker_0
# demo_logger_error.py

from sheenflow import job, op


@op
def hello_logs_error(context):
    raise Exception("Somebody set up us the bomb")


@job
def demo_job_error():
    hello_logs_error()


# end_builtin_logger_error_marker_0


defs = Definitions(jobs=[demo_job, demo_job_error])
