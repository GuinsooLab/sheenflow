from sheenflow._core.utils import check_dagster_package_version

from .configs import define_spark_config
from .ops import create_spark_op
from .resources import spark_resource
from .types import SparkOpError
from .utils import construct_spark_shell_command
from .version import __version__

check_dagster_package_version("sheenflow-spark", __version__)

__all__ = [
    "construct_spark_shell_command",
    "define_spark_config",
    "spark_resource",
    "SparkOpError",
]
