import time

import kubernetes
import pytest
from sheenflow_k8s.client import DagsterK8sError, DagsterKubernetesClient, WaitForPodState

pytest_plugins = ["dagster_k8s_test_infra.helm"]


def construct_pod_spec(name, cmd):
    return kubernetes.client.V1PodSpec(
        restart_policy="Never",
        containers=[
            kubernetes.client.V1Container(name=name, image="busybox", args=["/bin/sh", "-c", cmd])
        ],
    )


def construct_pod_manifest(name, cmd):
    return kubernetes.client.V1Pod(
        metadata=kubernetes.client.V1ObjectMeta(name=name),
        spec=construct_pod_spec(name, cmd),
    )


def construct_job_manifest(name, cmd):
    return kubernetes.client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=kubernetes.client.V1ObjectMeta(name=name),
        spec=kubernetes.client.V1JobSpec(
            template=kubernetes.client.V1PodTemplateSpec(spec=construct_pod_spec(name, cmd)),
        ),
    )


@pytest.mark.default
def test_wait_for_pod(cluster_provider, namespace):  # pylint: disable=unused-argument
    api_client = DagsterKubernetesClient.production_client()

    # Without this sleep, we get the following error on kind:
    # HTTP response body:
    # {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"No API
    # token found for service account \"default\", retry after the token is automatically
    # created and added to the service
    # account","reason":"ServerTimeout","details":{"name":"create
    # pod","kind":"serviceaccounts","retryAfterSeconds":1},"code":500}
    time.sleep(5)

    try:
        api_client.core_api.create_namespaced_pod(
            body=construct_pod_manifest("sayhi1", 'echo "hello world"'), namespace=namespace
        )
        api_client.wait_for_pod("sayhi1", namespace=namespace)
        assert api_client.retrieve_pod_logs("sayhi1", namespace=namespace) == "hello world\n"

        api_client.core_api.create_namespaced_pod(
            body=construct_pod_manifest("sayhi2", 'echo "hello world"'), namespace=namespace
        )
        api_client.wait_for_pod(
            "sayhi2", namespace=namespace, wait_for_state=WaitForPodState.Terminated
        )

        with pytest.raises(
            DagsterK8sError, match="Timed out while waiting for pod to become ready"
        ):
            api_client.core_api.create_namespaced_pod(
                body=construct_pod_manifest("sayhi3", 'sleep 5; echo "hello world"'),
                namespace=namespace,
            )
            api_client.wait_for_pod("sayhi3", namespace=namespace, wait_timeout=1)

        with pytest.raises(DagsterK8sError) as exc_info:
            api_client.core_api.create_namespaced_pod(
                body=construct_pod_manifest("fail", 'echo "whoops!"; exit 1'),
                namespace=namespace,
            )
            api_client.wait_for_pod(
                "fail", namespace=namespace, wait_for_state=WaitForPodState.Terminated
            )

        # not doing total match because integration test. unit tests test full log message
        assert "Pod did not exit successfully." in str(exc_info.value)

    finally:
        for pod_name in ["sayhi1", "sayhi2", "sayhi3", "fail"]:
            try:
                api_client.core_api.delete_namespaced_pod(pod_name, namespace=namespace)
            except kubernetes.client.rest.ApiException:
                pass


@pytest.mark.default
def test_wait_for_job(cluster_provider, namespace):  # pylint: disable=unused-argument
    # Without this sleep, we get the following error on kind:
    # HTTP response body:
    # {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"No API
    # token found for service account \"default\", retry after the token is automatically
    # created and added to the service
    # account","reason":"ServerTimeout","details":{"name":"create
    # pod","kind":"serviceaccounts","retryAfterSeconds":1},"code":500}
    time.sleep(5)

    try:
        api_client = DagsterKubernetesClient.production_client()

        api_client.batch_api.create_namespaced_job(
            body=construct_job_manifest("sayhi1", 'echo "hello world"'), namespace=namespace
        )
        api_client.wait_for_job_success("sayhi1", namespace=namespace)

        with pytest.raises(
            DagsterK8sError, match="Timed out while waiting for job sayhi2 to complete"
        ):
            api_client.batch_api.create_namespaced_job(
                body=construct_job_manifest("sayhi2", 'sleep 5; echo "hello world"'),
                namespace=namespace,
            )
            api_client.wait_for_job_success("sayhi2", namespace=namespace, wait_timeout=1)

        with pytest.raises(
            DagsterK8sError,
            match="Encountered failed job pods for job fail with status:",
        ):
            api_client.batch_api.create_namespaced_job(
                body=construct_job_manifest("fail", 'echo "whoops!"; exit 1'),
                namespace=namespace,
            )
            api_client.wait_for_job_success("fail", namespace=namespace)

    finally:
        for job in ["sayhi1", "sayhi2", "fail"]:
            try:
                api_client.batch_api.delete_namespaced_job(
                    job, namespace=namespace, propagation_policy="Foreground"
                )
            except kubernetes.client.rest.ApiException:
                pass
