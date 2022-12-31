import pytest

from sheenflow._core.test_utils import instance_for_test
from sheenflow._core.workspace.context import WorkspaceProcessContext
from sheenflow._core.workspace.load import load_workspace_process_context_from_yaml_paths
from sheenflow._utils import file_relative_path


@pytest.fixture
def instance():
    with instance_for_test() as instance:
        yield instance


def test_load_in_process_location_hello_world_terse(instance):
    with load_workspace_process_context_from_yaml_paths(
        instance,
        [file_relative_path(__file__, "terse_python_module_workspace.yaml")],
    ) as workspace:
        assert isinstance(workspace, WorkspaceProcessContext)
        assert workspace.repository_locations_count == 1
        assert workspace.repository_location_names[0] == "sheenflow.utils.test.hello_world_repository"


def test_load_in_process_location_hello_world_nested(instance):
    with load_workspace_process_context_from_yaml_paths(
        instance,
        [file_relative_path(__file__, "nested_python_module_workspace.yaml")],
    ) as workspace:
        assert isinstance(workspace, WorkspaceProcessContext)
        assert workspace.repository_locations_count == 1
        assert workspace.repository_location_names[0] == "sheenflow.utils.test.hello_world_repository"


def test_load_in_process_location_hello_world_nested_with_def(instance):
    with load_workspace_process_context_from_yaml_paths(
        instance,
        [file_relative_path(__file__, "nested_with_def_python_module_workspace.yaml")],
    ) as workspace:
        assert isinstance(workspace, WorkspaceProcessContext)
        assert workspace.repository_locations_count == 1
        assert (
            workspace.repository_location_names[0]
            == "sheenflow.utils.test.hello_world_repository:hello_world_repository"
        )
