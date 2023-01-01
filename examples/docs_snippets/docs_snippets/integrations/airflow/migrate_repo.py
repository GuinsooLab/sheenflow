import os

from sheenflow_airflow import make_dagster_repo_from_airflow_dags_path

migrated_airflow_repo = make_dagster_repo_from_airflow_dags_path(
    os.path.join(os.getenv("AIRFLOW_HOME"), "dags"),
    "migrated_airflow_repo",
)
