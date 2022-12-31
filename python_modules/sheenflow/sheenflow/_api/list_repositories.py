from typing import TYPE_CHECKING, Optional

import sheenflow._check as check
from sheenflow._core.errors import DagsterUserCodeProcessError
from sheenflow._core.types.loadable_target_origin import LoadableTargetOrigin
from sheenflow._grpc.types import ListRepositoriesResponse
from sheenflow._serdes import deserialize_as
from sheenflow._utils.error import SerializableErrorInfo

if TYPE_CHECKING:
    from sheenflow._grpc.client import DagsterGrpcClient


def sync_list_repositories_grpc(api_client: "DagsterGrpcClient") -> ListRepositoriesResponse:
    from sheenflow._grpc.client import DagsterGrpcClient

    check.inst_param(api_client, "api_client", DagsterGrpcClient)
    result = deserialize_as(
        api_client.list_repositories(),
        (ListRepositoriesResponse, SerializableErrorInfo),
    )
    if isinstance(result, SerializableErrorInfo):
        raise DagsterUserCodeProcessError(
            result.to_string(), user_code_process_error_infos=[result]
        )
    else:
        return result


def sync_list_repositories_ephemeral_grpc(
    executable_path: str,
    python_file: Optional[str],
    module_name: Optional[str],
    working_directory: Optional[str],
    attribute: Optional[str],
    package_name: Optional[str],
) -> ListRepositoriesResponse:
    from sheenflow._grpc.client import ephemeral_grpc_api_client

    check.str_param(executable_path, "executable_path")
    check.opt_str_param(python_file, "python_file")
    check.opt_str_param(module_name, "module_name")
    check.opt_str_param(working_directory, "working_directory")
    check.opt_str_param(attribute, "attribute")
    check.opt_str_param(package_name, "package_name")

    with ephemeral_grpc_api_client(
        loadable_target_origin=LoadableTargetOrigin(
            executable_path=executable_path,
            module_name=module_name,
            python_file=python_file,
            working_directory=working_directory,
            attribute=attribute,
            package_name=package_name,
        )
    ) as api_client:
        return sync_list_repositories_grpc(api_client)
