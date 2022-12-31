from sheenflow._core.utils import check_dagster_package_version

from .version import __version__

check_dagster_package_version("sheenflow_aws", __version__)
