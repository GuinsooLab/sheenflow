import logging
import os

from sheenflow_airflow_tests.marks import requires_airflow_db
from sheenflow_airflow_tests.test_factory.utils import validate_pipeline_execution
from sheenflow_airflow_tests.test_fixtures import (  # pylint: disable=unused-import
    dagster_airflow_custom_operator_pipeline,
)
from sheenflow_test.sheenflow_airflow.custom_operator import CustomOperator
from sheenflow_test.test_project import get_test_project_environments_path

from sheenflow._core.definitions.reconstruct import ReconstructableRepository


@requires_airflow_db
def test_my_custom_operator(
    dagster_airflow_custom_operator_pipeline,
    caplog,
):  # pylint: disable=redefined-outer-name
    caplog.set_level(logging.INFO, logger="CustomOperatorLogger")
    pipeline_name = "demo_pipeline_s3"
    operator = CustomOperator

    environments_path = get_test_project_environments_path()

    results = dagster_airflow_custom_operator_pipeline(
        pipeline_name=pipeline_name,
        recon_repo=ReconstructableRepository.for_module(
            "sheenflow_test.test_project.test_pipelines.repo", pipeline_name
        ),
        operator=operator,
        environment_yaml=[
            os.path.join(environments_path, "env.yaml"),
            os.path.join(environments_path, "env_s3.yaml"),
        ],
    )
    validate_pipeline_execution(results)

    log_lines = 0
    for record in caplog.records:
        if record.name == "CustomOperatorLogger":
            log_lines += 1
            assert record.message == "CustomOperator is called"

    assert log_lines == 2
