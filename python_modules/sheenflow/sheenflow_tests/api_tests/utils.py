import sys
from contextlib import ExitStack, contextmanager

from dagster import file_relative_path
from sheenflow._core.host_representation import (
    JobHandle,
    ManagedGrpcPythonEnvRepositoryLocationOrigin,
)
from sheenflow._core.test_utils import instance_for_test
from sheenflow._core.types.loadable_target_origin import LoadableTargetOrigin
from sheenflow._core.workspace.context import WorkspaceProcessContext
from sheenflow._core.workspace.load_target import PythonFileTarget


@contextmanager
def get_bar_workspace(instance):
    with WorkspaceProcessContext(
        instance,
        PythonFileTarget(
            python_file=file_relative_path(__file__, "api_tests_repo.py"),
            attribute="bar_repo",
            working_directory=None,
            location_name="bar_repo_location",
        ),
    ) as workspace_process_context:
        yield workspace_process_context.create_request_context()


@contextmanager
def get_bar_repo_repository_location(instance=None):
    with ExitStack() as stack:
        if not instance:
            instance = stack.enter_context(instance_for_test())

        loadable_target_origin = LoadableTargetOrigin(
            executable_path=sys.executable,
            python_file=file_relative_path(__file__, "api_tests_repo.py"),
            attribute="bar_repo",
        )
        location_name = "bar_repo_location"

        origin = ManagedGrpcPythonEnvRepositoryLocationOrigin(loadable_target_origin, location_name)

        with origin.create_single_location(instance) as location:
            yield location


@contextmanager
def get_bar_repo_handle(instance=None):
    with ExitStack() as stack:
        if not instance:
            instance = stack.enter_context(instance_for_test())

        with get_bar_repo_repository_location(instance) as location:
            yield location.get_repository("bar_repo").handle


@contextmanager
def get_foo_job_handle(instance=None):

    with ExitStack() as stack:
        if not instance:
            instance = stack.enter_context(instance_for_test())

        with get_bar_repo_handle(instance) as repo_handle:
            yield JobHandle("foo", repo_handle)
