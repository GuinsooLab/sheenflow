from sheenflow._core.utils import check_dagster_package_version

from .executor import celery_executor
from .version import __version__

check_dagster_package_version("sheenflow-celery", __version__)

__all__ = ["celery_executor"]
