import kubernetes
import pytest
from sheenflow_k8s import execute_k8s_job, k8s_job_op
from sheenflow_k8s.client import DagsterK8sError, DagsterKubernetesClient
from sheenflow_k8s.job import get_k8s_job_name

from sheenflow import job, op


def _get_pod_logs(cluster_provider, job_name, namespace):
    kubernetes.config.load_kube_config(cluster_provider.kubeconfig_file)
    api_client = DagsterKubernetesClient.production_client()
    pod_names = api_client.get_pod_names_in_job(job_name, namespace=namespace)
    return api_client.retrieve_pod_logs(pod_names[0], namespace=namespace)


@pytest.mark.default
def test_k8s_job_op(namespace, cluster_provider):
    first_op = k8s_job_op.configured(
        {
            "image": "busybox",
            "command": ["/bin/sh", "-c"],
            "args": ["echo HI"],
            "namespace": namespace,
            "load_incluster_config": False,
            "kubeconfig_file": cluster_provider.kubeconfig_file,
        },
        name="first_op",
    )
    second_op = k8s_job_op.configured(
        {
            "image": "busybox",
            "command": ["/bin/sh", "-c"],
            "args": ["echo GOODBYE"],
            "namespace": namespace,
            "load_incluster_config": False,
            "kubeconfig_file": cluster_provider.kubeconfig_file,
        },
        name="second_op",
    )

    @job
    def my_full_job():
        second_op(first_op())

    execute_result = my_full_job.execute_in_process()
    assert execute_result.success

    run_id = execute_result.dagster_run.run_id
    job_name = get_k8s_job_name(run_id, first_op.name)
    assert "HI" in _get_pod_logs(cluster_provider, job_name, namespace)

    job_name = get_k8s_job_name(run_id, second_op.name)
    assert "GOODBYE" in _get_pod_logs(cluster_provider, job_name, namespace)


@pytest.mark.default
def test_custom_k8s_op(namespace, cluster_provider):
    @op
    def my_custom_op(context):
        execute_k8s_job(
            context,
            image="busybox",
            command=["/bin/sh", "-c"],
            args=["echo HI"],
            namespace=namespace,
            load_incluster_config=False,
            kubeconfig_file=cluster_provider.kubeconfig_file,
        )
        return "GOODBYE"

    @op
    def my_second_custom_op(context, what_to_echo: str):
        execute_k8s_job(
            context,
            image="busybox",
            command=["/bin/sh", "-c"],
            args=[f"echo {what_to_echo}"],
            namespace=namespace,
            load_incluster_config=False,
            kubeconfig_file=cluster_provider.kubeconfig_file,
        )

    @job
    def my_job_with_custom_ops():
        my_second_custom_op(my_custom_op())

    execute_result = my_job_with_custom_ops.execute_in_process()
    assert execute_result.success

    run_id = execute_result.dagster_run.run_id
    job_name = get_k8s_job_name(run_id, my_custom_op.name)
    assert "HI" in _get_pod_logs(cluster_provider, job_name, namespace)

    job_name = get_k8s_job_name(run_id, my_second_custom_op.name)
    assert "GOODBYE" in _get_pod_logs(cluster_provider, job_name, namespace)


@pytest.mark.default
def test_k8s_job_op_with_timeout_success(namespace, cluster_provider):
    first_op = k8s_job_op.configured(
        {
            "image": "busybox",
            "command": ["/bin/sh", "-c"],
            "args": ["echo HI"],
            "namespace": namespace,
            "load_incluster_config": False,
            "kubeconfig_file": cluster_provider.kubeconfig_file,
            "timeout": 600,
        },
        name="first_op",
    )

    @job
    def my_full_job():
        first_op()

    execute_result = my_full_job.execute_in_process()
    assert execute_result.success

    run_id = execute_result.dagster_run.run_id
    job_name = get_k8s_job_name(run_id, first_op.name)
    assert "HI" in _get_pod_logs(cluster_provider, job_name, namespace)


@pytest.mark.default
def test_k8s_job_op_with_timeout_fail(namespace, cluster_provider):
    timeout_op = k8s_job_op.configured(
        {
            "image": "busybox",
            "command": ["/bin/sh", "-c"],
            "args": ["sleep 15 && echo HI"],
            "namespace": namespace,
            "load_incluster_config": False,
            "kubeconfig_file": cluster_provider.kubeconfig_file,
            "timeout": 5,
        },
        name="timeout_op",
    )

    @job
    def timeout_job():
        timeout_op()

    with pytest.raises(DagsterK8sError, match="Timed out while waiting for pod to become ready"):
        timeout_job.execute_in_process()


@pytest.mark.default
def test_k8s_job_op_with_failure(namespace, cluster_provider):
    failure_op = k8s_job_op.configured(
        {
            "image": "busybox",
            "command": ["/bin/sh", "-c"],
            "args": ["sleep 10 && exit 1"],
            "namespace": namespace,
            "load_incluster_config": False,
            "kubeconfig_file": cluster_provider.kubeconfig_file,
            "timeout": 5,
        },
        name="failure_op",
    )

    @job
    def failure_job():
        failure_op()

    with pytest.raises(DagsterK8sError, match="Timed out while waiting for pod to become ready"):
        failure_job.execute_in_process()


@pytest.mark.default
def test_k8s_job_op_with_container_config(namespace, cluster_provider):
    with_container_config = k8s_job_op.configured(
        {
            "image": "busybox",
            "container_config": {"command": ["echo", "SHELL_FROM_CONTAINER_CONFIG"]},
            "namespace": namespace,
            "load_incluster_config": False,
            "kubeconfig_file": cluster_provider.kubeconfig_file,
        },
        name="with_container_config",
    )

    @job
    def with_config_job():
        with_container_config()

    execute_result = with_config_job.execute_in_process()
    run_id = execute_result.dagster_run.run_id
    job_name = get_k8s_job_name(run_id, with_container_config.name)

    assert "SHELL_FROM_CONTAINER_CONFIG" in _get_pod_logs(cluster_provider, job_name, namespace)
