import os

import pytest
from airflow.exceptions import AirflowException
from sheenflow_airflow.factory import DagsterOperatorParameters
from sheenflow_airflow.operators.docker_operator import DagsterDockerOperator
from sheenflow_airflow_tests.marks import requires_airflow_db

from sheenflow import repository
from sheenflow._core.definitions.reconstruct import ReconstructableRepository
from sheenflow._core.execution.api import create_execution_plan
from sheenflow._core.snap import snapshot_from_execution_plan
from sheenflow._core.test_utils import default_mode_def_for_test, instance_for_test
from sheenflow._legacy import pipeline, solid
from sheenflow._utils import file_relative_path


@solid
def nonce_solid(_):
    return


@pipeline(mode_defs=[default_mode_def_for_test])
def nonce_pipeline():
    return nonce_solid()


@repository
def my_repository():
    return [nonce_pipeline]


nonce_pipeline_snapshot = nonce_pipeline.get_pipeline_snapshot()

nonce_execution_plan_snapshot = snapshot_from_execution_plan(
    create_execution_plan(nonce_pipeline), nonce_pipeline.get_pipeline_snapshot_id()
)

recon_repo_for_tests = ReconstructableRepository.for_file(
    file_relative_path(__file__, "test_dagster_docker_operator.py"),
    "my_repository",
)


def test_init_modified_docker_operator(dagster_docker_image):
    with instance_for_test() as instance:
        dagster_operator_parameters = DagsterOperatorParameters(
            task_id="nonce",
            pipeline_name="nonce_pipeline",
            mode="default",
            op_kwargs={
                "image": dagster_docker_image,
                "api_version": "auto",
            },
            pipeline_snapshot=nonce_pipeline_snapshot,
            execution_plan_snapshot=nonce_execution_plan_snapshot,
            instance_ref=instance.get_ref(),
            recon_repo=recon_repo_for_tests,
        )
        DagsterDockerOperator(dagster_operator_parameters=dagster_operator_parameters)


@requires_airflow_db
def test_modified_docker_operator_bad_docker_conn(dagster_docker_image):
    with instance_for_test() as instance:
        dagster_operator_parameters = DagsterOperatorParameters(
            task_id="nonce",
            pipeline_name="nonce_pipeline",
            mode="default",
            op_kwargs={
                "image": dagster_docker_image,
                "api_version": "auto",
                "docker_conn_id": "foo_conn",
                "command": "sheenflow --help",
            },
            pipeline_snapshot=nonce_pipeline_snapshot,
            execution_plan_snapshot=nonce_execution_plan_snapshot,
            instance_ref=instance.get_ref(),
            recon_repo=recon_repo_for_tests,
        )
        operator = DagsterDockerOperator(dagster_operator_parameters=dagster_operator_parameters)

        with pytest.raises(AirflowException, match="The conn_id `foo_conn` isn't defined"):
            operator.execute({})


def test_modified_docker_operator_env(dagster_docker_image):
    with instance_for_test() as instance:
        dagster_operator_parameters = DagsterOperatorParameters(
            task_id="nonce",
            pipeline_name="nonce_pipeline",
            mode="default",
            op_kwargs={
                "image": dagster_docker_image,
                "api_version": "auto",
                "command": "sheenflow --help",
            },
            pipeline_snapshot=nonce_pipeline_snapshot,
            execution_plan_snapshot=nonce_execution_plan_snapshot,
            instance_ref=instance.get_ref(),
            recon_repo=recon_repo_for_tests,
        )
        operator = DagsterDockerOperator(dagster_operator_parameters=dagster_operator_parameters)
        with pytest.raises(AirflowException, match="Could not parse response"):
            operator.execute({})


def test_modified_docker_operator_bad_command(dagster_docker_image):
    with instance_for_test() as instance:
        dagster_operator_parameters = DagsterOperatorParameters(
            task_id="nonce",
            pipeline_name="nonce_pipeline",
            mode="default",
            op_kwargs={
                "image": dagster_docker_image,
                "api_version": "auto",
                "command": "sheenflow gargle bargle",
            },
            pipeline_snapshot=nonce_pipeline_snapshot,
            execution_plan_snapshot=nonce_execution_plan_snapshot,
            instance_ref=instance.get_ref(),
            recon_repo=recon_repo_for_tests,
        )
        operator = DagsterDockerOperator(dagster_operator_parameters=dagster_operator_parameters)
        with pytest.raises(AirflowException, match="Usage: sheenflow"):
            operator.execute({})


def test_modified_docker_operator_url(dagster_docker_image):
    try:
        docker_host = os.getenv("DOCKER_HOST")
        docker_tls_verify = os.getenv("DOCKER_TLS_VERIFY")
        docker_cert_path = os.getenv("DOCKER_CERT_PATH")

        os.environ["DOCKER_HOST"] = "gargle"
        os.environ["DOCKER_TLS_VERIFY"] = "bargle"
        os.environ["DOCKER_CERT_PATH"] = "farfle"

        with instance_for_test() as instance:
            dagster_operator_parameters = DagsterOperatorParameters(
                task_id="nonce",
                pipeline_name="nonce_pipeline",
                mode="default",
                op_kwargs={
                    "image": dagster_docker_image,
                    "api_version": "auto",
                    "docker_url": docker_host or "unix:///var/run/docker.sock",
                    "tls_hostname": docker_host if docker_tls_verify else False,
                    "tls_ca_cert": docker_cert_path,
                    "command": "sheenflow --help",
                },
                pipeline_snapshot=nonce_pipeline_snapshot,
                execution_plan_snapshot=nonce_execution_plan_snapshot,
                instance_ref=instance.get_ref(),
                recon_repo=recon_repo_for_tests,
            )
            operator = DagsterDockerOperator(
                dagster_operator_parameters=dagster_operator_parameters
            )

            with pytest.raises(AirflowException, match="Could not parse response"):
                operator.execute({})

    finally:
        if docker_host is not None:
            os.environ["DOCKER_HOST"] = docker_host
        else:
            del os.environ["DOCKER_HOST"]

        if docker_tls_verify is not None:
            os.environ["DOCKER_TLS_VERIFY"] = docker_tls_verify
        else:
            del os.environ["DOCKER_TLS_VERIFY"]

        if docker_cert_path is not None:
            os.environ["DOCKER_CERT_PATH"] = docker_cert_path or ""
        else:
            del os.environ["DOCKER_CERT_PATH"]
