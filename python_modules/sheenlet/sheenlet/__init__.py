from sheenflow._core.utils import check_dagster_package_version

from .version import __version__

check_dagster_package_version("sheenlet", __version__)
