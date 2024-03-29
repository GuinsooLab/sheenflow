import sys
from types import ModuleType

import sheenflow._module_alias_map as _module_alias_map

# Imports of a key will return the module named by the corresponding value.
sys.meta_path.insert(
    _module_alias_map.get_meta_path_insertion_index(),
    _module_alias_map.AliasedModuleFinder(
        {
            "sheenflow.api": "sheenflow._api",
            "sheenflow.builtins": "sheenflow._builtins",
            "sheenflow.check": "sheenflow._check",
            "sheenflow.cli": "sheenflow._cli",
            "sheenflow.config": "sheenflow._config",
            "sheenflow.core": "sheenflow._core",
            "sheenflow.daemon": "sheenflow._daemon",
            "sheenflow.experimental": "sheenflow._experimental",
            "sheenflow.generate": "sheenflow._generate",
            "sheenflow.grpc": "sheenflow._grpc",
            "sheenflow.loggers": "sheenflow._loggers",
            "sheenflow.serdes": "sheenflow._serdes",
            "sheenflow.seven": "sheenflow._seven",
            "sheenflow.utils": "sheenflow._utils",
        }
    ),
)

# ########################
# ##### NOTES ON IMPORT FORMAT
# ########################
#
# This file defines sheenflow's public API. Imports need to be structured/formatted so as to to ensure
# that the broadest possible set of static analyzers understand Dagster's
# public API as intended. The below guidelines ensure this is the case.
#
# (1) All imports in this module intended to define exported symbols should be of the form `from
# sheenflow.foo import X as X`. This is because imported symbols are not by default considered public
# by static analyzers. The redundant alias form `import X as X` overwrites the private imported `X`
# with a public `X` bound to the same value. It is also possible to expose `X` as public by listing
# it inside `__all__`, but the redundant alias form is preferred here due to easier maintainability
# and shorter file length.

# (2) All imports should target the module in which a symbol is actually defined, rather than a
# container module where it is imported. This rule also derives from the default private status of
# imported symbols. So long as there is a private import somewhere in the import chain leading from
# an import to its definition, some linters will be triggered (e.g. pyright). For example, the
# following results in a linter error when using sheenflow as a third-party library:

#     ### sheenflow/foo/bar.py
#     BAR = "BAR"
#
#     ### sheenflow/foo/__init__.py
#     from .bar import BAR  # BAR is imported so it is not part of sheenflow.foo public interface
#     FOO = "FOO"
#
#     ### sheenflow/__init__.py
#     from .foo import FOO, BAR  # importing BAR is importing a private symbol from sheenflow.foo
#     __all__ = ["FOO", "BAR"]
#
#     ### some_user_code.py
#     # from sheenflow import BAR  # linter error even though `BAR` is in `sheenflow.__all__`!
#
# We could get around this by always remembering to use the `from .foo import X as X` form in containers, but
# it is simpler to just import directly from the defining module.

# Turn off isort here so that we keep nice one-import-per-line formatting
# isort: off

from sheenflow._builtins import (
    Any as Any,
    Bool as Bool,
    Float as Float,
    Int as Int,
    Nothing as Nothing,
    String as String,
)
from sheenflow._config.config_schema import (
    ConfigSchema as ConfigSchema,
)
from sheenflow._config.config_type import (
    Array as Array,
    Enum as Enum,
    EnumValue as EnumValue,
    Noneable as Noneable,
    ScalarUnion as ScalarUnion,
)
from sheenflow._config.field import (
    Field as Field,
)
from sheenflow._config.field_utils import (
    Map as Map,
    Permissive as Permissive,
    Selector as Selector,
    Shape as Shape,
)
from sheenflow._config.source import (
    BoolSource as BoolSource,
    IntSource as IntSource,
    StringSource as StringSource,
)

from sheenflow._core.definitions.asset_in import (
    AssetIn as AssetIn,
)
from sheenflow._core.definitions.asset_out import (
    AssetOut as AssetOut,
)
from sheenflow._core.definitions.asset_selection import (
    AssetSelection as AssetSelection,
)
from sheenflow._core.definitions.asset_sensor_definition import (
    AssetSensorDefinition as AssetSensorDefinition,
)
from sheenflow._core.definitions.assets import (
    AssetsDefinition as AssetsDefinition,
)
from sheenflow._core.definitions.config import (
    ConfigMapping as ConfigMapping,
)
from sheenflow._core.definitions.composition import (
    PendingNodeInvocation as PendingNodeInvocation,
)
from sheenflow._core.definitions.configurable import (
    configured as configured,
)
from sheenflow._core.definitions.decorators.asset_decorator import (
    asset as asset,
    multi_asset as multi_asset,
)
from sheenflow._core.definitions.decorators.config_mapping_decorator import (
    config_mapping as config_mapping,
)
from sheenflow._core.definitions.decorators.graph_decorator import (
    graph as graph,
)
from sheenflow._core.definitions.decorators.hook_decorator import (
    failure_hook as failure_hook,
    success_hook as success_hook,
)
from sheenflow._core.definitions.decorators.job_decorator import (
    job as job,
)
from sheenflow._core.definitions.decorators.op_decorator import (
    op as op,
)
from sheenflow._core.definitions.decorators.repository_decorator import (
    repository as repository,
)
from sheenflow._core.definitions.decorators.schedule_decorator import (
    schedule as schedule,
)
from sheenflow._core.definitions.decorators.sensor_decorator import (
    asset_sensor as asset_sensor,
    sensor as sensor,
    multi_asset_sensor as multi_asset_sensor,
)
from sheenflow._core.definitions.decorators.source_asset_decorator import (
    observable_source_asset as observable_source_asset,
)
from sheenflow._core.definitions.dependency import (
    DependencyDefinition as DependencyDefinition,
    MultiDependencyDefinition as MultiDependencyDefinition,
    NodeInvocation as NodeInvocation,
)
from sheenflow._core.definitions.definitions_class import Definitions as Definitions
from sheenflow._core.definitions.events import (
    AssetKey as AssetKey,
    AssetMaterialization as AssetMaterialization,
    AssetObservation as AssetObservation,
    DynamicOutput as DynamicOutput,
    ExpectationResult as ExpectationResult,
    Failure as Failure,
    Output as Output,
    RetryRequested as RetryRequested,
    TypeCheck as TypeCheck,
)
from sheenflow._core.definitions.executor_definition import (
    ExecutorDefinition as ExecutorDefinition,
    ExecutorRequirement as ExecutorRequirement,
    executor as executor,
    in_process_executor as in_process_executor,
    multi_or_in_process_executor as multi_or_in_process_executor,
    multiple_process_executor_requirements as multiple_process_executor_requirements,
    multiprocess_executor as multiprocess_executor,
)
from sheenflow._core.definitions.freshness_policy import (
    FreshnessPolicy as FreshnessPolicy,
)
from sheenflow._core.definitions.freshness_policy_sensor_definition import (
    FreshnessPolicySensorContext as FreshnessPolicySensorContext,
    FreshnessPolicySensorDefinition as FreshnessPolicySensorDefinition,
    build_freshness_policy_sensor_context as build_freshness_policy_sensor_context,
    freshness_policy_sensor as freshness_policy_sensor,
)
from sheenflow._core.definitions.graph_definition import (
    GraphDefinition as GraphDefinition,
)
from sheenflow._core.definitions.hook_definition import (
    HookDefinition as HookDefinition,
)
from sheenflow._core.definitions.input import (
    GraphIn as GraphIn,
    In as In,
    InputMapping as InputMapping,
)
from sheenflow._core.definitions.job_definition import (
    JobDefinition as JobDefinition,
)
from sheenflow._core.definitions.load_assets_from_modules import (
    load_assets_from_current_module as load_assets_from_current_module,
    load_assets_from_modules as load_assets_from_modules,
    load_assets_from_package_module as load_assets_from_package_module,
    load_assets_from_package_name as load_assets_from_package_name,
)
from sheenflow._core.definitions.logger_definition import (
    LoggerDefinition as LoggerDefinition,
    build_init_logger_context as build_init_logger_context,
    logger as logger,
)
from sheenflow._core.definitions.logical_version import (
    LogicalVersion as LogicalVersion,
)
from sheenflow._core.definitions.materialize import (
    materialize as materialize,
    materialize_to_memory as materialize_to_memory,
)
from sheenflow._core.definitions.metadata import (
    BoolMetadataValue as BoolMetadataValue,
    DagsterAssetMetadataValue as DagsterAssetMetadataValue,
    DagsterRunMetadataValue as DagsterRunMetadataValue,
    FloatMetadataValue as FloatMetadataValue,
    IntMetadataValue as IntMetadataValue,
    JsonMetadataValue as JsonMetadataValue,
    MarkdownMetadataValue as MarkdownMetadataValue,
    MetadataEntry as MetadataEntry,
    MetadataValue as MetadataValue,
    NotebookMetadataValue as NotebookMetadataValue,
    PathMetadataValue as PathMetadataValue,
    PythonArtifactMetadataValue as PythonArtifactMetadataValue,
    TableMetadataValue as TableMetadataValue,
    TableSchemaMetadataValue as TableSchemaMetadataValue,
    TextMetadataValue as TextMetadataValue,
    UrlMetadataValue as UrlMetadataValue,
)
from sheenflow._core.definitions.metadata.table import (
    TableColumn as TableColumn,
    TableColumnConstraints as TableColumnConstraints,
    TableConstraints as TableConstraints,
    TableRecord as TableRecord,
    TableSchema as TableSchema,
)
from sheenflow._core.definitions.multi_asset_sensor_definition import (
    MultiAssetSensorDefinition as MultiAssetSensorDefinition,
    MultiAssetSensorEvaluationContext as MultiAssetSensorEvaluationContext,
    build_multi_asset_sensor_context as build_multi_asset_sensor_context,
)
from sheenflow._core.definitions.op_definition import (
    OpDefinition as OpDefinition,
)
from sheenflow._core.definitions.output import (
    DynamicOut as DynamicOut,
    GraphOut as GraphOut,
    Out as Out,
    OutputMapping as OutputMapping,
)
from sheenflow._core.definitions.partition import (
    DynamicPartitionsDefinition as DynamicPartitionsDefinition,
    Partition as Partition,
    PartitionScheduleDefinition as PartitionScheduleDefinition,
    PartitionedConfig as PartitionedConfig,
    PartitionsDefinition as PartitionsDefinition,
    StaticPartitionsDefinition as StaticPartitionsDefinition,
    dynamic_partitioned_config as dynamic_partitioned_config,
    static_partitioned_config as static_partitioned_config,
)
from sheenflow._core.definitions.partition_key_range import (
    PartitionKeyRange as PartitionKeyRange,
)
from sheenflow._core.definitions.partition_mapping import (
    AllPartitionMapping as AllPartitionMapping,
    IdentityPartitionMapping as IdentityPartitionMapping,
    LastPartitionMapping as LastPartitionMapping,
    PartitionMapping as PartitionMapping,
)
from sheenflow._core.definitions.partitioned_schedule import (
    build_schedule_from_partitioned_job as build_schedule_from_partitioned_job,
)
from sheenflow._core.definitions.policy import (
    Backoff as Backoff,
    Jitter as Jitter,
    RetryPolicy as RetryPolicy,
)
from sheenflow._core.definitions.reconstruct import (
    build_reconstructable_job as build_reconstructable_job,
    reconstructable as reconstructable,
)
from sheenflow._core.definitions.repository_definition import (
    RepositoryData as RepositoryData,
    RepositoryDefinition as RepositoryDefinition,
)
from sheenflow._core.definitions.resource_definition import (
    ResourceDefinition as ResourceDefinition,
    make_values_resource as make_values_resource,
    resource as resource,
)
from sheenflow._core.definitions.run_request import (
    RunRequest as RunRequest,
    SkipReason as SkipReason,
)
from sheenflow._core.definitions.run_status_sensor_definition import (
    RunFailureSensorContext as RunFailureSensorContext,
    RunStatusSensorContext as RunStatusSensorContext,
    RunStatusSensorDefinition as RunStatusSensorDefinition,
    build_run_status_sensor_context as build_run_status_sensor_context,
    run_failure_sensor as run_failure_sensor,
    run_status_sensor as run_status_sensor,
)
from sheenflow._core.definitions.schedule_definition import (
    DefaultScheduleStatus as DefaultScheduleStatus,
    ScheduleDefinition as ScheduleDefinition,
    ScheduleEvaluationContext as ScheduleEvaluationContext,
    build_schedule_context as build_schedule_context,
)
from sheenflow._core.definitions.sensor_definition import (
    DefaultSensorStatus as DefaultSensorStatus,
    SensorDefinition as SensorDefinition,
    SensorEvaluationContext as SensorEvaluationContext,
    build_sensor_context as build_sensor_context,
)
from sheenflow._core.definitions.source_asset import (
    SourceAsset as SourceAsset,
)
from sheenflow._core.definitions.step_launcher import (
    StepLauncher as StepLauncher,
    StepRunRef as StepRunRef,
)
from sheenflow._core.definitions.time_window_partition_mapping import (
    TimeWindowPartitionMapping as TimeWindowPartitionMapping,
)
from sheenflow._core.definitions.time_window_partitions import (
    DailyPartitionsDefinition as DailyPartitionsDefinition,
    HourlyPartitionsDefinition as HourlyPartitionsDefinition,
    MonthlyPartitionsDefinition as MonthlyPartitionsDefinition,
    TimeWindow as TimeWindow,
    TimeWindowPartitionsDefinition as TimeWindowPartitionsDefinition,
    WeeklyPartitionsDefinition as WeeklyPartitionsDefinition,
    daily_partitioned_config as daily_partitioned_config,
    hourly_partitioned_config as hourly_partitioned_config,
    monthly_partitioned_config as monthly_partitioned_config,
    weekly_partitioned_config as weekly_partitioned_config,
)
from sheenflow._core.definitions.multi_dimensional_partitions import (
    MultiPartitionsDefinition as MultiPartitionsDefinition,
    MultiPartitionKey as MultiPartitionKey,
)
from sheenflow._core.definitions.unresolved_asset_job_definition import (
    define_asset_job as define_asset_job,
)

from sheenflow._core.definitions.asset_reconciliation_sensor import (
    build_asset_reconciliation_sensor as build_asset_reconciliation_sensor,
)
from sheenflow._core.definitions.utils import (
    config_from_files as config_from_files,
    config_from_pkg_resources as config_from_pkg_resources,
    config_from_yaml_strings as config_from_yaml_strings,
)
from sheenflow._core.definitions.version_strategy import (
    OpVersionContext as OpVersionContext,
    ResourceVersionContext as ResourceVersionContext,
    SourceHashVersionStrategy as SourceHashVersionStrategy,
    VersionStrategy as VersionStrategy,
)
from sheenflow._core.errors import (
    DagsterConfigMappingFunctionError as DagsterConfigMappingFunctionError,
    DagsterError as DagsterError,
    DagsterEventLogInvalidForRun as DagsterEventLogInvalidForRun,
    DagsterExecutionInterruptedError as DagsterExecutionInterruptedError,
    DagsterExecutionStepExecutionError as DagsterExecutionStepExecutionError,
    DagsterExecutionStepNotFoundError as DagsterExecutionStepNotFoundError,
    DagsterInvalidConfigDefinitionError as DagsterInvalidConfigDefinitionError,
    DagsterInvalidConfigError as DagsterInvalidConfigError,
    DagsterInvalidDefinitionError as DagsterInvalidDefinitionError,
    DagsterInvalidInvocationError as DagsterInvalidInvocationError,
    DagsterInvalidSubsetError as DagsterInvalidSubsetError,
    DagsterInvariantViolationError as DagsterInvariantViolationError,
    DagsterResourceFunctionError as DagsterResourceFunctionError,
    DagsterRunNotFoundError as DagsterRunNotFoundError,
    DagsterStepOutputNotFoundError as DagsterStepOutputNotFoundError,
    DagsterSubprocessError as DagsterSubprocessError,
    DagsterTypeCheckDidNotPass as DagsterTypeCheckDidNotPass,
    DagsterTypeCheckError as DagsterTypeCheckError,
    DagsterUnknownPartitionError as DagsterUnknownPartitionError,
    DagsterUnknownResourceError as DagsterUnknownResourceError,
    DagsterUnmetExecutorRequirementsError as DagsterUnmetExecutorRequirementsError,
    DagsterUserCodeExecutionError as DagsterUserCodeExecutionError,
    raise_execution_interrupts as raise_execution_interrupts,
)
from sheenflow._core.events import (
    DagsterEvent as DagsterEvent,
    DagsterEventType as DagsterEventType,
)
from sheenflow._core.events.log import (
    EventLogEntry as EventLogEntry,
)
from sheenflow._core.execution.api import (
    ReexecutionOptions as ReexecutionOptions,
    execute_job as execute_job,
)
from sheenflow._core.execution.build_resources import (
    build_resources as build_resources,
)
from sheenflow._core.execution.context.compute import (
    OpExecutionContext as OpExecutionContext,
)
from sheenflow._core.execution.context.hook import (
    HookContext as HookContext,
    build_hook_context as build_hook_context,
)
from sheenflow._core.execution.context.init import (
    InitResourceContext as InitResourceContext,
    build_init_resource_context as build_init_resource_context,
)
from sheenflow._core.execution.context.input import (
    InputContext as InputContext,
    build_input_context as build_input_context,
)
from sheenflow._core.execution.context.invocation import (
    build_op_context as build_op_context,
)
from sheenflow._core.execution.context.logger import (
    InitLoggerContext as InitLoggerContext,
)
from sheenflow._core.execution.context.output import (
    OutputContext as OutputContext,
    build_output_context as build_output_context,
)
from sheenflow._core.execution.context.system import (
    TypeCheckContext as TypeCheckContext,
)
from sheenflow._core.execution.execute_in_process_result import (
    ExecuteInProcessResult as ExecuteInProcessResult,
)
from sheenflow._core.execution.execute_job_result import (
    ExecuteJobResult as ExecuteJobResult,
)
from sheenflow._core.execution.plan.external_step import (
    external_instance_from_step_run_ref as external_instance_from_step_run_ref,
    run_step_from_ref as run_step_from_ref,
    step_context_to_step_run_ref as step_context_to_step_run_ref,
    step_run_ref_to_step_context as step_run_ref_to_step_context,
)
from sheenflow._core.execution.validate_run_config import (
    validate_run_config as validate_run_config,
)
from sheenflow._core.execution.with_resources import (
    with_resources as with_resources,
)
from sheenflow._core.executor.base import (
    Executor as Executor,
)
from sheenflow._core.executor.init import (
    InitExecutorContext as InitExecutorContext,
)

from sheenflow._core.host_representation.selector import (
    CodeLocationSelector as CodeLocationSelector,
    RepositorySelector as RepositorySelector,
    JobSelector as JobSelector,
)
from sheenflow._core.instance import (
    DagsterInstance as DagsterInstance,
)
from sheenflow._core.launcher.default_run_launcher import (
    DefaultRunLauncher as DefaultRunLauncher,
)
from sheenflow._core.log_manager import (
    DagsterLogManager as DagsterLogManager,
)

from sheenflow._core.event_api import (
    EventLogRecord as EventLogRecord,
    EventRecordsFilter as EventRecordsFilter,
    RunShardedEventsCursor as RunShardedEventsCursor,
)
from sheenflow._core.storage.asset_value_loader import (
    AssetValueLoader as AssetValueLoader,
)
from sheenflow._core.storage.file_manager import (
    FileHandle as FileHandle,
    LocalFileHandle as LocalFileHandle,
    local_file_manager as local_file_manager,
)
from sheenflow._core.storage.fs_io_manager import (
    custom_path_fs_io_manager as custom_path_fs_io_manager,
    fs_io_manager as fs_io_manager,
)
from sheenflow._core.storage.input_manager import (
    InputManager as InputManager,
    input_manager as input_manager,
)
from sheenflow._core.storage.io_manager import (
    IOManager as IOManager,
    IOManagerDefinition as IOManagerDefinition,
    io_manager as io_manager,
)
from sheenflow._core.storage.mem_io_manager import (
    InMemoryIOManager as InMemoryIOManager,
    mem_io_manager as mem_io_manager,
)
from sheenflow._core.storage.memoizable_io_manager import (
    MemoizableIOManager as MemoizableIOManager,
)
from sheenflow._core.storage.pipeline_run import (
    DagsterRun as DagsterRun,
    DagsterRunStatus as DagsterRunStatus,
    RunsFilter as RunsFilter,
    RunRecord as RunRecord,
)
from sheenflow._core.storage.root_input_manager import (
    RootInputManager as RootInputManager,
    RootInputManagerDefinition as RootInputManagerDefinition,
    root_input_manager as root_input_manager,
)
from sheenflow._core.storage.tags import (
    MEMOIZED_RUN_TAG as MEMOIZED_RUN_TAG,
)
from sheenflow._core.types.config_schema import (
    DagsterTypeLoader as DagsterTypeLoader,
    dagster_type_loader as dagster_type_loader,
)
from sheenflow._core.test_utils import instance_for_test
from sheenflow._core.types.dagster_type import (
    DagsterType as DagsterType,
    List as List,
    Optional as Optional,
    PythonObjectDagsterType as PythonObjectDagsterType,
    make_python_type_usable_as_dagster_type as make_python_type_usable_as_dagster_type,
)
from sheenflow._core.types.decorator import (
    usable_as_dagster_type as usable_as_dagster_type,
)
from sheenflow._core.types.python_dict import (
    Dict as Dict,
)
from sheenflow._core.types.python_set import (
    Set as Set,
)
from sheenflow._core.types.python_tuple import (
    Tuple as Tuple,
)
from sheenflow._loggers import (
    colored_console_logger as colored_console_logger,
    default_loggers as default_loggers,
    default_system_loggers as default_system_loggers,
    json_console_logger as json_console_logger,
)
from sheenflow._core.execution.context.system import (
    DagsterTypeLoaderContext as DagsterTypeLoaderContext,
    StepExecutionContext as StepExecutionContext,
)
from sheenflow._serdes.serdes import (
    deserialize_value as deserialize_value,
    serialize_value as serialize_value,
)
from sheenflow._core.storage.upath_io_manager import UPathIOManager as UPathIOManager
from sheenflow._utils import (
    file_relative_path as file_relative_path,
)
from sheenflow._utils.alert import (
    make_email_on_run_failure_sensor as make_email_on_run_failure_sensor,
)
from sheenflow._utils.backcompat import (
    ExperimentalWarning as ExperimentalWarning,
)
from sheenflow._utils.log import (
    get_dagster_logger as get_dagster_logger,
)

from sheenflow._utils.dagster_type import (
    check_dagster_type as check_dagster_type,
)

# isort: on

from sheenflow.version import __version__

# ########################
# ##### DYNAMIC IMPORTS
# ########################

# isort: split
import importlib
from typing import TYPE_CHECKING
from typing import Any as TypingAny
from typing import Callable, Mapping, Sequence
from typing import Tuple as TypingTuple

from typing_extensions import Final

from sheenflow._utils.backcompat import deprecation_warning, rename_warning

# NOTE: Unfortunately we have to declare deprecated aliases twice-- the
# TYPE_CHECKING declaration satisfies linters and type checkers, but the entry
# in `_DEPRECATED` is required  for us to generate the deprecation warning.

if TYPE_CHECKING:
    # pylint:disable=reimported
    from sheenflow._core.execution.context.system import DagsterTypeMaterializerContext
    from sheenflow._core.types.config_schema import DagsterTypeMaterializer, dagster_type_materializer

    # pylint:enable=reimported

_DEPRECATED: Final[Mapping[str, TypingTuple[str, str, str]]] = {
    "dagster_type_materializer": (
        "sheenflow._core.types.config_schema",
        "1.1.0",
        "Instead, use an IOManager.",
    ),
    "DagsterTypeMaterializer": (
        "sheenflow._core.types.config_schema",
        "1.1.0",
        "Instead, use an IOManager.",
    ),
    "DagsterTypeMaterializerContext": (
        "sheenflow._core.execution.context.system",
        "1.1.0",
        "Instead, use an IOManager.",
    ),
}

# Example Deprecated Renamed Entry:
#
# "EventMetadataEntry": (MetadataEntry, "1.0.0"),
_DEPRECATED_RENAMED: Final[Mapping[str, TypingTuple[Callable, str]]] = {}


def __getattr__(name: str) -> TypingAny:
    if name in _DEPRECATED:
        module, breaking_version, additional_warn_text = _DEPRECATED[name]
        value = getattr(importlib.import_module(module), name)
        stacklevel = 3 if sys.version_info >= (3, 7) else 4
        deprecation_warning(name, breaking_version, additional_warn_text, stacklevel=stacklevel)
        return value
    elif name in _DEPRECATED_RENAMED:
        value, breaking_version = _DEPRECATED_RENAMED[name]
        stacklevel = 3 if sys.version_info >= (3, 7) else 4
        rename_warning(value.__name__, name, breaking_version, stacklevel=stacklevel)
        return value
    else:
        raise AttributeError("module '{}' has no attribute '{}'".format(__name__, name))


def __dir__(_self: ModuleType) -> Sequence[str]:
    return [*globals(), *_DEPRECATED.keys(), *_DEPRECATED_RENAMED.keys()]
