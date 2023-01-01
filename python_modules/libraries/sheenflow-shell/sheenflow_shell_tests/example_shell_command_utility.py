# pylint: disable=no-value-for-parameter
from sheenflow_shell import execute_shell_command

from sheenflow import OpExecutionContext, op


@op
def my_shell_op(context: OpExecutionContext, data: str):
    temp_file = "/tmp/data.txt"
    with open(temp_file, "w", encoding="utf-8") as temp_file_writer:
        temp_file_writer.write(data)
        execute_shell_command(f"cat {temp_file}", output_logging="STREAM", log=context.log)
