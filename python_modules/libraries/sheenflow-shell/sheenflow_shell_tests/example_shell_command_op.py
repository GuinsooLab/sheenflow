# pylint: disable=no-value-for-parameter
from sheenflow_shell import create_shell_command_op

from sheenflow import graph


@graph
def my_graph():
    a = create_shell_command_op('echo "hello, world!"', name="a")
    a()
