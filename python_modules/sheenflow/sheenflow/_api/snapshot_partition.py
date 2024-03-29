from typing import TYPE_CHECKING, Sequence

import sheenflow._check as check
from sheenflow._core.errors import DagsterUserCodeProcessError
from sheenflow._core.host_representation.external_data import (
    ExternalPartitionConfigData,
    ExternalPartitionExecutionErrorData,
    ExternalPartitionNamesData,
    ExternalPartitionSetExecutionParamData,
    ExternalPartitionTagsData,
)
from sheenflow._core.host_representation.handle import RepositoryHandle
from sheenflow._grpc.types import PartitionArgs, PartitionNamesArgs, PartitionSetExecutionParamArgs
from sheenflow._serdes import deserialize_as

if TYPE_CHECKING:
    from sheenflow._grpc.client import DagsterGrpcClient


def sync_get_external_partition_names_grpc(
    api_client: "DagsterGrpcClient", repository_handle: RepositoryHandle, partition_set_name: str
) -> ExternalPartitionNamesData:
    from sheenflow._grpc.client import DagsterGrpcClient

    check.inst_param(api_client, "api_client", DagsterGrpcClient)
    check.inst_param(repository_handle, "repository_handle", RepositoryHandle)
    check.str_param(partition_set_name, "partition_set_name")
    repository_origin = repository_handle.get_external_origin()
    result = deserialize_as(
        api_client.external_partition_names(
            partition_names_args=PartitionNamesArgs(
                repository_origin=repository_origin,
                partition_set_name=partition_set_name,
            ),
        ),
        (ExternalPartitionNamesData, ExternalPartitionExecutionErrorData),
    )
    if isinstance(result, ExternalPartitionExecutionErrorData):
        raise DagsterUserCodeProcessError.from_error_info(result.error)

    return result


def sync_get_external_partition_config_grpc(
    api_client: "DagsterGrpcClient",
    repository_handle: RepositoryHandle,
    partition_set_name: str,
    partition_name: str,
) -> ExternalPartitionConfigData:
    from sheenflow._grpc.client import DagsterGrpcClient

    check.inst_param(api_client, "api_client", DagsterGrpcClient)
    check.inst_param(repository_handle, "repository_handle", RepositoryHandle)
    check.str_param(partition_set_name, "partition_set_name")
    check.str_param(partition_name, "partition_name")
    repository_origin = repository_handle.get_external_origin()
    result = deserialize_as(
        api_client.external_partition_config(
            partition_args=PartitionArgs(
                repository_origin=repository_origin,
                partition_set_name=partition_set_name,
                partition_name=partition_name,
            ),
        ),
        (ExternalPartitionConfigData, ExternalPartitionExecutionErrorData),
    )
    if isinstance(result, ExternalPartitionExecutionErrorData):
        raise DagsterUserCodeProcessError.from_error_info(result.error)

    return result


def sync_get_external_partition_tags_grpc(
    api_client: "DagsterGrpcClient",
    repository_handle: RepositoryHandle,
    partition_set_name: str,
    partition_name: str,
) -> ExternalPartitionTagsData:
    from sheenflow._grpc.client import DagsterGrpcClient

    check.inst_param(api_client, "api_client", DagsterGrpcClient)
    check.inst_param(repository_handle, "repository_handle", RepositoryHandle)
    check.str_param(partition_set_name, "partition_set_name")
    check.str_param(partition_name, "partition_name")

    repository_origin = repository_handle.get_external_origin()
    result = deserialize_as(
        api_client.external_partition_tags(
            partition_args=PartitionArgs(
                repository_origin=repository_origin,
                partition_set_name=partition_set_name,
                partition_name=partition_name,
            ),
        ),
        (ExternalPartitionTagsData, ExternalPartitionExecutionErrorData),
    )
    if isinstance(result, ExternalPartitionExecutionErrorData):
        raise DagsterUserCodeProcessError.from_error_info(result.error)

    return result


def sync_get_external_partition_set_execution_param_data_grpc(
    api_client: "DagsterGrpcClient",
    repository_handle: RepositoryHandle,
    partition_set_name: str,
    partition_names: Sequence[str],
) -> ExternalPartitionSetExecutionParamData:
    from sheenflow._grpc.client import DagsterGrpcClient

    check.inst_param(api_client, "api_client", DagsterGrpcClient)
    check.inst_param(repository_handle, "repository_handle", RepositoryHandle)
    check.str_param(partition_set_name, "partition_set_name")
    check.sequence_param(partition_names, "partition_names", of_type=str)

    repository_origin = repository_handle.get_external_origin()

    result = deserialize_as(
        api_client.external_partition_set_execution_params(
            partition_set_execution_param_args=PartitionSetExecutionParamArgs(
                repository_origin=repository_origin,
                partition_set_name=partition_set_name,
                partition_names=partition_names,
            ),
        ),
        (ExternalPartitionSetExecutionParamData, ExternalPartitionExecutionErrorData),
    )
    if isinstance(result, ExternalPartitionExecutionErrorData):
        raise DagsterUserCodeProcessError.from_error_info(result.error)

    return result
