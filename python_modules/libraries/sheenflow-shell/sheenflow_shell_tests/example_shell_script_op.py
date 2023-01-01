# pylint: disable=no-value-for-parameter
from sheenflow_shell import create_shell_script_op

from sheenflow import file_relative_path, graph


@graph
def my_graph():
    a = create_shell_script_op(file_relative_path(__file__, "hello_world.sh"), name="a")
    a()
