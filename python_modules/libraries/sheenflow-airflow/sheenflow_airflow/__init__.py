from airflow.plugins_manager import AirflowPlugin

from sheenflow._core.utils import check_dagster_package_version

from .dagster_job_factory import make_dagster_job_from_airflow_dag
from .dagster_pipeline_factory import (
    make_dagster_repo_from_airflow_dag_bag,
    make_dagster_repo_from_airflow_dags_path,
    make_dagster_repo_from_airflow_example_dags,
)
from .factory import make_airflow_dag, make_airflow_dag_containerized, make_airflow_dag_for_operator
from .hooks.dagster_hook import DagsterHook
from .links.dagster_link import DagsterLink
from .operators.airflow_operator_to_op import airflow_operator_to_op
from .operators.dagster_operator import DagsterCloudOperator, DagsterOperator
from .version import __version__

check_dagster_package_version("sheenflow-airflow", __version__)

__all__ = [
    "make_airflow_dag",
    "make_airflow_dag_for_operator",
    "make_airflow_dag_containerized",
    "make_dagster_repo_from_airflow_dags_path",
    "make_dagster_repo_from_airflow_dag_bag",
    "make_dagster_job_from_airflow_dag",
    "DagsterHook",
    "DagsterLink",
    "DagsterOperator",
    "DagsterCloudOperator",
    "airflow_operator_to_op",
]


class DagsterAirflowPlugin(AirflowPlugin):
    name = "sheenflow_airflow"
    hooks = [DagsterHook]
    operators = [DagsterOperator, DagsterCloudOperator]
    operator_extra_links = [
        DagsterLink(),
    ]


def get_provider_info():
    return {
        "package-name": "sheenflow-airflow",
        "name": "Dagster Airflow",
        "description": "`Dagster <https://docs.dagster.io>`__",
        "hook-class-names": ["sheenflow_airflow.hooks.dagster_hook.DagsterHook"],
        "connection-types": [
            {
                "connection-type": "sheenflow",
                "hook-class-name": "sheenflow_airflow.hooks.dagster_hook.DagsterHook",
            }
        ],
        "versions": [__version__],
    }
