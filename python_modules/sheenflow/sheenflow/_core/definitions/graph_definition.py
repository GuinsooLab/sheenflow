# pyright: strict

from collections import OrderedDict, defaultdict
from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from toposort import CircularDependencyError, toposort_flatten

import sheenflow._check as check
from sheenflow._annotations import public
from sheenflow._core.definitions.config import ConfigMapping
from sheenflow._core.definitions.definition_config_schema import IDefinitionConfigSchema
from sheenflow._core.definitions.policy import RetryPolicy
from sheenflow._core.definitions.resource_definition import ResourceDefinition
from sheenflow._core.errors import DagsterInvalidDefinitionError
from sheenflow._core.selector.subset_selector import AssetSelectionData
from sheenflow._core.types.dagster_type import (
    DagsterType,
    DagsterTypeKind,
    construct_dagster_type_dictionary,
)

from .dependency import (
    DependencyStructure,
    GraphNode,
    IDependencyDefinition,
    Node,
    NodeHandle,
    NodeInput,
    NodeInvocation,
)
from .hook_definition import HookDefinition
from .input import FanInInputPointer, InputDefinition, InputMapping, InputPointer
from .logger_definition import LoggerDefinition
from .metadata import MetadataEntry, PartitionMetadataEntry, RawMetadataValue
from .node_definition import NodeDefinition
from .output import OutputDefinition, OutputMapping
from .resource_requirement import ResourceRequirement
from .solid_container import create_execution_structure, validate_dependency_dict
from .version_strategy import VersionStrategy

if TYPE_CHECKING:
    from sheenflow._core.execution.execute_in_process_result import ExecuteInProcessResult
    from sheenflow._core.instance import DagsterInstance

    from .asset_layer import AssetLayer
    from .composition import PendingNodeInvocation
    from .executor_definition import ExecutorDefinition
    from .job_definition import JobDefinition
    from .op_definition import OpDefinition
    from .partition import PartitionedConfig, PartitionsDefinition


def _check_node_defs_arg(
    graph_name: str, node_defs: Optional[Sequence[NodeDefinition]]
) -> Sequence[NodeDefinition]:
    node_defs = node_defs or []

    _node_defs = check.opt_sequence_param(node_defs, "node_defs")
    for node_def in _node_defs:
        if isinstance(node_def, NodeDefinition):  # type: ignore
            continue
        elif callable(node_def):
            raise DagsterInvalidDefinitionError(
                """You have passed a lambda or function {func} into {name} that is
                not a node. You have likely forgetten to annotate this function with
                the @op or @graph decorators.'
                """.format(
                    name=graph_name, func=node_def.__name__
                )
            )
        else:
            raise DagsterInvalidDefinitionError(
                "Invalid item in node list: {item}".format(item=repr(node_def))
            )

    return node_defs


def _create_adjacency_lists(
    nodes: Sequence[Node],
    dep_structure: DependencyStructure,
) -> Tuple[Mapping[str, Set[str]], Mapping[str, Set[str]]]:
    visit_dict = {s.name: False for s in nodes}
    forward_edges: Dict[str, Set[str]] = {s.name: set() for s in nodes}
    backward_edges: Dict[str, Set[str]] = {s.name: set() for s in nodes}

    def visit(node_name: str) -> None:
        if visit_dict[node_name]:
            return

        visit_dict[node_name] = True

        for node_output in dep_structure.all_upstream_outputs_from_node(node_name):
            forward_node = node_output.node.name
            backward_node = node_name
            if forward_node in forward_edges:
                forward_edges[forward_node].add(backward_node)
                backward_edges[backward_node].add(forward_node)
                visit(forward_node)

    for s in nodes:
        visit(s.name)

    return (forward_edges, backward_edges)


class GraphDefinition(NodeDefinition):
    """Defines a Dagster graph.

    A graph is made up of

    - Nodes, which can either be an op (the functional unit of computation), or another graph.
    - Dependencies, which determine how the values produced by nodes as outputs flow from
      one node to another. This tells Dagster how to arrange nodes into a directed, acyclic graph
      (DAG) of compute.

    End users should prefer the :func:`@graph <graph>` decorator. GraphDefinition is generally
    intended to be used by framework authors or for programatically generated graphs.

    Args:
        name (str): The name of the graph. Must be unique within any :py:class:`GraphDefinition`
            or :py:class:`JobDefinition` containing the graph.
        description (Optional[str]): A human-readable description of the pipeline.
        node_defs (Optional[Sequence[NodeDefinition]]): The set of ops / graphs used in this graph.
        dependencies (Optional[Dict[Union[str, NodeInvocation], Dict[str, DependencyDefinition]]]):
            A structure that declares the dependencies of each op's inputs on the outputs of other
            ops in the graph. Keys of the top level dict are either the string names of ops in the
            graph or, in the case of aliased ops, :py:class:`NodeInvocations <NodeInvocation>`.
            Values of the top level dict are themselves dicts, which map input names belonging to
            the op or aliased op to :py:class:`DependencyDefinitions <DependencyDefinition>`.
        input_mappings (Optional[Sequence[InputMapping]]): Defines the inputs to the nested graph, and
            how they map to the inputs of its constituent ops.
        output_mappings (Optional[Sequence[OutputMapping]]): Defines the outputs of the nested graph,
            and how they map from the outputs of its constituent ops.
        config (Optional[ConfigMapping]): Defines the config of the graph, and how its schema maps
            to the config of its constituent ops.
        tags (Optional[Dict[str, Any]]): Arbitrary metadata for any execution of the graph.
            Values that are not strings will be json encoded and must meet the criteria that
            `json.loads(json.dumps(value)) == value`.  These tag values may be overwritten by tag
            values provided at invocation time.

    Examples:

        .. code-block:: python

            @op
            def return_one():
                return 1

            @op
            def add_one(num):
                return num + 1

            graph_def = GraphDefinition(
                name='basic',
                node_defs=[return_one, add_one],
                dependencies={'add_one': {'num': DependencyDefinition('return_one')}},
            )
    """

    _node_defs: Sequence[NodeDefinition]
    _dagster_type_dict: Mapping[str, DagsterType]
    _dependencies: Mapping[Union[str, NodeInvocation], Mapping[str, IDependencyDefinition]]
    _dependency_structure: DependencyStructure
    _node_dict: Mapping[str, Node]
    _input_mappings: Sequence[InputMapping]
    _output_mappings: Sequence[OutputMapping]
    _config_mapping: Optional[ConfigMapping]
    _nodes_in_topological_order: Sequence[Node]

    def __init__(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        node_defs: Optional[Sequence[NodeDefinition]] = None,
        dependencies: Optional[
            Mapping[Union[str, NodeInvocation], Mapping[str, IDependencyDefinition]]
        ] = None,
        input_mappings: Optional[Sequence[InputMapping]] = None,
        output_mappings: Optional[Sequence[OutputMapping]] = None,
        config: Optional[ConfigMapping] = None,
        tags: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        self._node_defs = _check_node_defs_arg(name, node_defs)
        self._dependencies = validate_dependency_dict(dependencies)
        self._dependency_structure, self._node_dict = create_execution_structure(
            self._node_defs, self._dependencies, graph_definition=self
        )

        # Sequence[InputMapping]
        self._input_mappings = check.opt_sequence_param(input_mappings, "input_mappings")
        input_defs = _validate_in_mappings(
            self._input_mappings,
            self._node_dict,
            self._dependency_structure,
            name,
            class_name=type(self).__name__,
        )

        # Sequence[OutputMapping]
        self._output_mappings, output_defs = _validate_out_mappings(
            check.opt_sequence_param(output_mappings, "output_mappings"),
            self._node_dict,
            name,
            class_name=type(self).__name__,
        )

        self._config_mapping = check.opt_inst_param(config, "config", ConfigMapping)

        super(GraphDefinition, self).__init__(
            name=name,
            description=description,
            input_defs=input_defs,
            output_defs=output_defs,
            tags=tags,
            **kwargs,
        )

        # must happen after base class construction as properties are assumed to be there
        # eager computation to detect cycles
        self._nodes_in_topological_order = self._get_nodes_in_topological_order()
        self._dagster_type_dict = construct_dagster_type_dictionary([self])

    def _get_nodes_in_topological_order(self) -> Sequence[Node]:

        _forward_edges, backward_edges = _create_adjacency_lists(
            self.solids, self.dependency_structure
        )

        try:
            order = toposort_flatten(backward_edges)
        except CircularDependencyError as err:
            raise DagsterInvalidDefinitionError(str(err)) from err

        return [self.solid_named(solid_name) for solid_name in order]

    def get_inputs_must_be_resolved_top_level(
        self, asset_layer: "AssetLayer", handle: Optional[NodeHandle] = None
    ) -> Sequence[InputDefinition]:
        unresolveable_input_defs = []
        for node in self.node_dict.values():
            cur_handle = NodeHandle(node.name, handle)
            for input_def in node.definition.get_inputs_must_be_resolved_top_level(
                asset_layer, cur_handle
            ):
                if self.dependency_structure.has_deps(NodeInput(node, input_def)):
                    continue
                elif not node.container_maps_input(input_def.name):
                    raise DagsterInvalidDefinitionError(
                        f"Input '{input_def.name}' of {node.describe_node()} "
                        "has no way of being resolved. Must provide a resolution to this "
                        "input via another op/graph, or via a direct input value mapped from the "
                        "top-level graph. To "
                        "learn more, see the docs for unconnected inputs: "
                        "https://docs.dagster.io/concepts/io-management/unconnected-inputs#unconnected-inputs."
                    )
                else:
                    mapped_input = node.container_mapped_input(input_def.name)
                    unresolveable_input_defs.append(mapped_input.get_definition())
        return unresolveable_input_defs

    @property
    def node_type_str(self) -> str:
        return "graph"

    @property
    def is_graph_job_op_node(self) -> bool:
        return True

    @property
    def solids(self) -> Sequence[Node]:
        return list(set(self._node_dict.values()))

    @property
    def node_dict(self) -> Mapping[str, Node]:
        return self._node_dict

    @property
    def node_defs(self) -> Sequence[NodeDefinition]:
        return self._node_defs

    @property
    def solids_in_topological_order(self) -> Sequence[Node]:
        return self._nodes_in_topological_order

    def has_solid_named(self, name: str) -> bool:
        check.str_param(name, "name")
        return name in self._node_dict

    def solid_named(self, name: str) -> Node:
        check.str_param(name, "name")
        check.invariant(
            name in self._node_dict,
            "{graph_name} has no op named {name}.".format(graph_name=self._name, name=name),
        )

        return self._node_dict[name]

    def get_solid(self, handle: NodeHandle) -> Node:
        check.inst_param(handle, "handle", NodeHandle)
        current = handle
        lineage: List[str] = []
        while current:
            lineage.append(current.name)
            current = current.parent

        name = lineage.pop()
        solid = self.solid_named(name)
        while lineage:
            name = lineage.pop()
            # We know that this is a current solid is a graph while ascending lineage
            definition = cast(GraphDefinition, solid.definition)
            solid = definition.solid_named(name)

        return solid

    def iterate_node_defs(self) -> Iterator[NodeDefinition]:
        yield self
        for outer_node_def in self._node_defs:
            yield from outer_node_def.iterate_node_defs()

    def iterate_solid_defs(self) -> Iterator["OpDefinition"]:
        for outer_node_def in self._node_defs:
            yield from outer_node_def.iterate_solid_defs()

    def iterate_node_handles(
        self, parent_node_handle: Optional[NodeHandle] = None
    ) -> Iterator[NodeHandle]:
        for node in self.node_dict.values():
            cur_node_handle = NodeHandle(node.name, parent_node_handle)
            if isinstance(node, GraphNode):
                graph_def = node.definition.ensure_graph_def()
                yield from graph_def.iterate_node_handles(cur_node_handle)
            yield cur_node_handle

    @public  # type: ignore
    @property
    def input_mappings(self) -> Sequence[InputMapping]:
        return self._input_mappings

    @public  # type: ignore
    @property
    def output_mappings(self) -> Sequence[OutputMapping]:
        return self._output_mappings

    @public  # type: ignore
    @property
    def config_mapping(self) -> Optional[ConfigMapping]:
        return self._config_mapping

    @property
    def has_config_mapping(self) -> bool:
        return self._config_mapping is not None

    def all_dagster_types(self) -> Iterable[DagsterType]:
        return self._dagster_type_dict.values()

    def has_dagster_type(self, name: str) -> bool:
        check.str_param(name, "name")
        return name in self._dagster_type_dict

    def dagster_type_named(self, name: str) -> DagsterType:
        check.str_param(name, "name")
        return self._dagster_type_dict[name]

    def get_input_mapping(self, input_name: str) -> InputMapping:

        check.str_param(input_name, "input_name")
        for mapping in self._input_mappings:
            if mapping.graph_input_name == input_name:
                return mapping
        check.failed(f"Could not find input mapping {input_name}")

    def input_mapping_for_pointer(
        self, pointer: Union[InputPointer, FanInInputPointer]
    ) -> Optional[InputMapping]:
        check.inst_param(pointer, "pointer", (InputPointer, FanInInputPointer))

        for mapping in self._input_mappings:
            if mapping.maps_to == pointer:
                return mapping
        return None

    def get_output_mapping(self, output_name: str) -> OutputMapping:
        check.str_param(output_name, "output_name")
        for mapping in self._output_mappings:
            if mapping.graph_output_name == output_name:
                return mapping
        check.failed(f"Could not find output mapping {output_name}")

    T_Handle = TypeVar("T_Handle", bound=Optional[NodeHandle])

    def resolve_output_to_origin(
        self, output_name: str, handle: Optional[NodeHandle]
    ) -> Tuple[OutputDefinition, Optional[NodeHandle]]:
        check.str_param(output_name, "output_name")
        check.opt_inst_param(handle, "handle", NodeHandle)

        mapping = self.get_output_mapping(output_name)
        check.invariant(mapping, "Can only resolve outputs for valid output names")
        mapped_solid = self.solid_named(mapping.maps_from.solid_name)
        return mapped_solid.definition.resolve_output_to_origin(
            mapping.maps_from.output_name,
            NodeHandle(mapped_solid.name, handle),  # type: ignore
        )

    def resolve_output_to_origin_op_def(self, output_name: str) -> "OpDefinition":
        mapping = self.get_output_mapping(output_name)
        check.invariant(mapping, "Can only resolve outputs for valid output names")
        return self.solid_named(
            mapping.maps_from.solid_name
        ).definition.resolve_output_to_origin_op_def(output_name)

    def default_value_for_input(self, input_name: str) -> object:
        check.str_param(input_name, "input_name")

        # base case
        if self.input_def_named(input_name).has_default_value:
            return self.input_def_named(input_name).default_value

        mapping = self.get_input_mapping(input_name)
        check.invariant(mapping, "Can only resolve inputs for valid input names")
        mapped_solid = self.solid_named(mapping.maps_to.solid_name)

        return mapped_solid.definition.default_value_for_input(mapping.maps_to.input_name)

    def input_has_default(self, input_name: str) -> bool:
        check.str_param(input_name, "input_name")

        # base case
        if self.input_def_named(input_name).has_default_value:
            return True

        mapping = self.get_input_mapping(input_name)
        check.invariant(mapping, "Can only resolve inputs for valid input names")
        mapped_solid = self.solid_named(mapping.maps_to.solid_name)

        return mapped_solid.definition.input_has_default(mapping.maps_to.input_name)

    @property
    def dependencies(
        self,
    ) -> Mapping[Union[str, NodeInvocation], Mapping[str, IDependencyDefinition]]:
        return self._dependencies

    @property
    def dependency_structure(self) -> DependencyStructure:
        return self._dependency_structure

    @property
    def config_schema(self) -> Optional[IDefinitionConfigSchema]:
        return self.config_mapping.config_schema if self.config_mapping is not None else None

    def input_supports_dynamic_output_dep(self, input_name: str) -> bool:
        mapping = self.get_input_mapping(input_name)
        target_node = mapping.maps_to.solid_name
        # check if input mapped to solid which is downstream of another dynamic output within
        if self.dependency_structure.is_dynamic_mapped(target_node):
            return False

        # check if input mapped to solid which starts new dynamic downstream
        if self.dependency_structure.has_dynamic_downstreams(target_node):
            return False

        return self.solid_named(target_node).definition.input_supports_dynamic_output_dep(
            mapping.maps_to.input_name
        )

    def copy_for_configured(
        self,
        name: str,
        description: Optional[str],
        config_schema: Any,
        config_or_config_fn: Any,
    ):
        if not self.has_config_mapping:
            raise DagsterInvalidDefinitionError(
                "Only graphs utilizing config mapping can be pre-configured. The graph "
                '"{graph_name}" does not have a config mapping, and thus has nothing to be '
                "configured.".format(graph_name=self.name)
            )
        config_mapping = cast(ConfigMapping, self.config_mapping)
        return GraphDefinition(
            name=name,
            description=check.opt_str_param(description, "description", default=self.description),
            node_defs=self._node_defs,
            dependencies=self._dependencies,
            input_mappings=self._input_mappings,
            output_mappings=self._output_mappings,
            config=ConfigMapping(
                config_mapping.config_fn,
                config_schema=config_schema,
                receive_processed_config_values=config_mapping.receive_processed_config_values,
            ),
        )

    def node_names(self):
        return list(self._node_dict.keys())

    @public
    def to_job(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        resource_defs: Optional[Mapping[str, ResourceDefinition]] = None,
        config: Optional[Union[ConfigMapping, Mapping[str, object], "PartitionedConfig"]] = None,
        tags: Optional[Mapping[str, str]] = None,
        metadata: Optional[Mapping[str, RawMetadataValue]] = None,
        logger_defs: Optional[Mapping[str, LoggerDefinition]] = None,
        executor_def: Optional["ExecutorDefinition"] = None,
        hooks: Optional[AbstractSet[HookDefinition]] = None,
        op_retry_policy: Optional[RetryPolicy] = None,
        version_strategy: Optional[VersionStrategy] = None,
        op_selection: Optional[Sequence[str]] = None,
        partitions_def: Optional["PartitionsDefinition"] = None,
        asset_layer: Optional["AssetLayer"] = None,
        input_values: Optional[Mapping[str, object]] = None,
        _asset_selection_data: Optional[AssetSelectionData] = None,
        _metadata_entries: Optional[Sequence[Union[MetadataEntry, PartitionMetadataEntry]]] = None,
    ) -> "JobDefinition":
        """
        Make this graph in to an executable Job by providing remaining components required for execution.

        Args:
            name (Optional[str]):
                The name for the Job. Defaults to the name of the this graph.
            resource_defs (Optional[Mapping [str, ResourceDefinition]]):
                Resources that are required by this graph for execution.
                If not defined, `io_manager` will default to filesystem.
            config:
                Describes how the job is parameterized at runtime.

                If no value is provided, then the schema for the job's run config is a standard
                format based on its solids and resources.

                If a dictionary is provided, then it must conform to the standard config schema, and
                it will be used as the job's run config for the job whenever the job is executed.
                The values provided will be viewable and editable in the Dagit playground, so be
                careful with secrets.

                If a :py:class:`ConfigMapping` object is provided, then the schema for the job's run config is
                determined by the config mapping, and the ConfigMapping, which should return
                configuration in the standard format to configure the job.

                If a :py:class:`PartitionedConfig` object is provided, then it defines a discrete set of config
                values that can parameterize the job, as well as a function for mapping those
                values to the base config. The values provided will be viewable and editable in the
                Dagit playground, so be careful with secrets.
            tags (Optional[Mapping[str, Any]]):
                Arbitrary information that will be attached to the execution of the Job.
                Values that are not strings will be json encoded and must meet the criteria that
                `json.loads(json.dumps(value)) == value`.  These tag values may be overwritten by tag
                values provided at invocation time.
            metadata (Optional[Mapping[str, RawMetadataValue]]):
                Arbitrary information that will be attached to the JobDefinition and be viewable in Dagit.
                Keys must be strings, and values must be python primitive types or one of the provided
                MetadataValue types
            logger_defs (Optional[Mapping[str, LoggerDefinition]]):
                A dictionary of string logger identifiers to their implementations.
            executor_def (Optional[ExecutorDefinition]):
                How this Job will be executed. Defaults to :py:class:`multi_or_in_process_executor`,
                which can be switched between multi-process and in-process modes of execution. The
                default mode of execution is multi-process.
            op_retry_policy (Optional[RetryPolicy]): The default retry policy for all ops in this job.
                Only used if retry policy is not defined on the op definition or op invocation.
            version_strategy (Optional[VersionStrategy]):
                Defines how each solid (and optionally, resource) in the job can be versioned. If
                provided, memoizaton will be enabled for this job.
            partitions_def (Optional[PartitionsDefinition]): Defines a discrete set of partition
                keys that can parameterize the job. If this argument is supplied, the config
                argument can't also be supplied.
            asset_layer (Optional[AssetLayer]): Top level information about the assets this job
                will produce. Generally should not be set manually.
            input_values (Optional[Mapping[str, Any]]):
                A dictionary that maps python objects to the top-level inputs of a job.

        Returns:
            JobDefinition
        """
        from .job_definition import JobDefinition

        return JobDefinition(
            name=name,
            description=description or self.description,
            graph_def=self,
            resource_defs=resource_defs,
            logger_defs=logger_defs,
            executor_def=executor_def,
            config=config,
            partitions_def=partitions_def,
            tags=tags,
            metadata=metadata,
            hook_defs=hooks,
            version_strategy=version_strategy,
            op_retry_policy=op_retry_policy,
            asset_layer=asset_layer,
            input_values=input_values,
            _subset_selection_data=_asset_selection_data,
            _metadata_entries=_metadata_entries,
        ).get_job_def_for_subset_selection(op_selection)

    def coerce_to_job(self):
        # attempt to coerce a Graph in to a Job, raising a useful error if it doesn't work
        try:
            return self.to_job()
        except DagsterInvalidDefinitionError as err:
            raise DagsterInvalidDefinitionError(
                f"Failed attempting to coerce Graph {self.name} in to a Job. "
                "Use to_job instead, passing the required information."
            ) from err

    @public
    def execute_in_process(
        self,
        run_config: Any = None,
        instance: Optional["DagsterInstance"] = None,
        resources: Optional[Mapping[str, object]] = None,
        raise_on_error: bool = True,
        op_selection: Optional[Sequence[str]] = None,
        run_id: Optional[str] = None,
        input_values: Optional[Mapping[str, object]] = None,
    ) -> "ExecuteInProcessResult":
        """
        Execute this graph in-process, collecting results in-memory.

        Args:
            run_config (Optional[Mapping[str, Any]]):
                Run config to provide to execution. The configuration for the underlying graph
                should exist under the "ops" key.
            instance (Optional[DagsterInstance]):
                The instance to execute against, an ephemeral one will be used if none provided.
            resources (Optional[Mapping[str, Any]]):
                The resources needed if any are required. Can provide resource instances directly,
                or resource definitions.
            raise_on_error (Optional[bool]): Whether or not to raise exceptions when they occur.
                Defaults to ``True``.
            op_selection (Optional[List[str]]): A list of op selection queries (including single op
                names) to execute. For example:
                * ``['some_op']``: selects ``some_op`` itself.
                * ``['*some_op']``: select ``some_op`` and all its ancestors (upstream dependencies).
                * ``['*some_op+++']``: select ``some_op``, all its ancestors, and its descendants
                (downstream dependencies) within 3 levels down.
                * ``['*some_op', 'other_op_a', 'other_op_b+']``: select ``some_op`` and all its
                ancestors, ``other_op_a`` itself, and ``other_op_b`` and its direct child ops.
            input_values (Optional[Mapping[str, Any]]):
                A dictionary that maps python objects to the top-level inputs of the graph.

        Returns:
            :py:class:`~sheenflow.ExecuteInProcessResult`
        """
        from sheenflow._core.execution.build_resources import wrap_resources_for_execution
        from sheenflow._core.instance import DagsterInstance

        from .executor_definition import execute_in_process_executor
        from .job_definition import JobDefinition

        instance = check.opt_inst_param(instance, "instance", DagsterInstance)
        resources = check.opt_mapping_param(resources, "resources", key_type=str)
        input_values = check.opt_mapping_param(input_values, "input_values")

        resource_defs = wrap_resources_for_execution(resources)

        ephemeral_job = JobDefinition(
            name=self._name,
            graph_def=self,
            executor_def=execute_in_process_executor,
            resource_defs=resource_defs,
            input_values=input_values,
        ).get_job_def_for_subset_selection(op_selection)

        run_config = run_config if run_config is not None else {}
        op_selection = check.opt_sequence_param(op_selection, "op_selection", str)

        return ephemeral_job.execute_in_process(
            run_config=run_config,
            instance=instance,
            raise_on_error=raise_on_error,
            run_id=run_id,
        )

    @property
    def parent_graph_def(self) -> Optional["GraphDefinition"]:
        return None

    @property
    def is_subselected(self) -> bool:
        return False

    def get_resource_requirements(
        self, asset_layer: Optional["AssetLayer"] = None
    ) -> Iterator[ResourceRequirement]:
        for node in self.node_dict.values():
            yield from node.get_resource_requirements(outer_container=self, asset_layer=asset_layer)

        for dagster_type in self.all_dagster_types():
            yield from sheenflow_type.get_resource_requirements()

    @public  # type: ignore
    @property
    def name(self) -> str:
        return super(GraphDefinition, self).name

    @public  # type: ignore
    @property
    def tags(self) -> Mapping[str, str]:
        return super(GraphDefinition, self).tags

    @public
    def alias(self, name: str) -> "PendingNodeInvocation":
        return super(GraphDefinition, self).alias(name)

    @public
    def tag(self, tags: Optional[Mapping[str, str]]) -> "PendingNodeInvocation":
        return super(GraphDefinition, self).tag(tags)

    @public
    def with_hooks(self, hook_defs: AbstractSet[HookDefinition]) -> "PendingNodeInvocation":
        return super(GraphDefinition, self).with_hooks(hook_defs)

    @public
    def with_retry_policy(self, retry_policy: RetryPolicy) -> "PendingNodeInvocation":
        return super(GraphDefinition, self).with_retry_policy(retry_policy)


class SubselectedGraphDefinition(GraphDefinition):
    """Defines a subselected graph.

    Args:
        parent_graph_def (GraphDefinition): The parent graph that this current graph is subselected
            from. This is used for tracking where the subselected graph originally comes from.
            Note that we allow subselecting a subselected graph, and this field refers to the direct
            parent graph of the current subselection, rather than the original root graph.
        node_defs (Optional[Sequence[NodeDefinition]]): A list of all top level nodes in the graph. A
            node can be an op or a graph that contains other nodes.
        dependencies (Optional[Mapping[Union[str, NodeInvocation], Mapping[str, IDependencyDefinition]]]):
            A structure that declares the dependencies of each op's inputs on the outputs of other
            ops in the subselected graph. Keys of the top level dict are either the string names of
            ops in the graph or, in the case of aliased solids, :py:class:`NodeInvocations <NodeInvocation>`.
            Values of the top level dict are themselves dicts, which map input names belonging to
            the op or aliased op to :py:class:`DependencyDefinitions <DependencyDefinition>`.
        input_mappings (Optional[Sequence[InputMapping]]): Define the inputs to the nested graph, and
            how they map to the inputs of its constituent ops.
        output_mappings (Optional[Sequence[OutputMapping]]): Define the outputs of the nested graph, and
            how they map from the outputs of its constituent ops.
    """

    def __init__(
        self,
        parent_graph_def: GraphDefinition,
        node_defs: Optional[Sequence[NodeDefinition]],
        dependencies: Optional[
            Mapping[Union[str, NodeInvocation], Mapping[str, IDependencyDefinition]]
        ],
        input_mappings: Optional[Sequence[InputMapping]],
        output_mappings: Optional[Sequence[OutputMapping]],
    ):
        self._parent_graph_def = check.inst_param(
            parent_graph_def, "parent_graph_def", GraphDefinition
        )
        super(SubselectedGraphDefinition, self).__init__(
            name=parent_graph_def.name,  # should we create special name for subselected graphs
            node_defs=node_defs,
            dependencies=dependencies,
            input_mappings=input_mappings,
            output_mappings=output_mappings,
            config=parent_graph_def.config_mapping,
            tags=parent_graph_def.tags,
        )

    @property
    def parent_graph_def(self) -> GraphDefinition:
        return self._parent_graph_def

    def get_top_level_omitted_nodes(self) -> Sequence[Node]:
        return [
            solid for solid in self.parent_graph_def.solids if not self.has_solid_named(solid.name)
        ]

    @property
    def is_subselected(self) -> bool:
        return True


def _validate_in_mappings(
    input_mappings: Sequence[InputMapping],
    nodes_by_name: Mapping[str, Node],
    dependency_structure: DependencyStructure,
    name: str,
    class_name: str,
) -> Sequence[InputDefinition]:
    from .composition import MappedInputPlaceholder

    input_defs_by_name: Dict[str, InputDefinition] = OrderedDict()
    mapping_keys = set()

    target_input_types_by_graph_input_name: Dict[str, Set[DagsterType]] = defaultdict(set)

    for mapping in input_mappings:
        # handle incorrect objects passed in as mappings
        if not isinstance(mapping, InputMapping):
            if isinstance(mapping, InputDefinition):
                raise DagsterInvalidDefinitionError(
                    f"In {class_name} '{name}' you passed an InputDefinition "
                    f"named '{mapping.name}' directly in to input_mappings. Return "
                    "an InputMapping by calling mapping_to on the InputDefinition."
                )
            else:
                raise DagsterInvalidDefinitionError(
                    f"In {class_name} '{name}' received unexpected type '{type(mapping)}' in input_mappings. "
                    "Provide an InputMapping using InputMapping(...)"
                )

        input_defs_by_name[mapping.graph_input_name] = mapping.get_definition()

        target_node = nodes_by_name.get(mapping.maps_to.node_name)
        if target_node is None:
            raise DagsterInvalidDefinitionError(
                f"In {class_name} '{name}' input mapping references node "
                f"'{mapping.maps_to.node_name}' which it does not contain."
            )
        if not target_node.has_input(mapping.maps_to.input_name):
            raise DagsterInvalidDefinitionError(
                f"In {class_name} '{name}' input mapping to node '{mapping.maps_to.node_name}' "
                f"which contains no input named '{mapping.maps_to.input_name}'"
            )

        target_input_def = target_node.input_def_named(mapping.maps_to.input_name)
        node_input = NodeInput(target_node, target_input_def)

        if mapping.maps_to_fan_in:
            maps_to = cast(FanInInputPointer, mapping.maps_to)
            if not dependency_structure.has_fan_in_deps(node_input):
                raise DagsterInvalidDefinitionError(
                    f"In {class_name} '{name}' input mapping target "
                    f'"{maps_to.node_name}.{maps_to.input_name}" (index {maps_to.fan_in_index} of fan-in) '
                    f"is not a MultiDependencyDefinition."
                )
            inner_deps = dependency_structure.get_fan_in_deps(node_input)
            if (maps_to.fan_in_index >= len(inner_deps)) or (
                inner_deps[maps_to.fan_in_index] is not MappedInputPlaceholder
            ):
                raise DagsterInvalidDefinitionError(
                    f"In {class_name} '{name}' input mapping target "
                    f'"{maps_to.node_name}.{maps_to.input_name}" index {maps_to.fan_in_index} in '
                    f"the MultiDependencyDefinition is not a MappedInputPlaceholder"
                )
            mapping_keys.add(f"{maps_to.node_name}.{maps_to.input_name}.{maps_to.fan_in_index}")
            target_input_types_by_graph_input_name[mapping.graph_input_name].add(
                target_input_def.dagster_type.get_inner_type_for_fan_in()
            )
        else:
            if dependency_structure.has_deps(node_input):
                raise DagsterInvalidDefinitionError(
                    f"In {class_name} '{name}' input mapping target "
                    f'"{mapping.maps_to.node_name}.{mapping.maps_to.input_name}" '
                    "is already satisfied by output"
                )

            mapping_keys.add(f"{mapping.maps_to.node_name}.{mapping.maps_to.input_name}")
            target_input_types_by_graph_input_name[mapping.graph_input_name].add(
                target_input_def.dagster_type
            )

    for node_input in dependency_structure.inputs():
        if dependency_structure.has_fan_in_deps(node_input):
            for idx, dep in enumerate(dependency_structure.get_fan_in_deps(node_input)):
                if dep is MappedInputPlaceholder:
                    mapping_str = f"{node_input.node_name}.{node_input.input_name}.{idx}"
                    if mapping_str not in mapping_keys:
                        raise DagsterInvalidDefinitionError(
                            f"Unsatisfied MappedInputPlaceholder at index {idx} in "
                            f"MultiDependencyDefinition for '{node_input.node_name}.{node_input.input_name}'"
                        )

    # if the sheenflow type on a graph input is Any and all its target inputs have the
    # same sheenflow type, then use that sheenflow type for the graph input
    for graph_input_name, graph_input_def in input_defs_by_name.items():
        if graph_input_def.dagster_type.kind == DagsterTypeKind.ANY:
            target_input_types = target_input_types_by_graph_input_name[graph_input_name]
            if len(target_input_types) == 1:
                input_defs_by_name[graph_input_name] = graph_input_def.with_dagster_type(
                    next(iter(target_input_types))
                )

    return list(input_defs_by_name.values())


def _validate_out_mappings(
    output_mappings: Sequence[OutputMapping],
    solid_dict: Mapping[str, Node],
    name: str,
    class_name: str,
) -> Tuple[Sequence[OutputMapping], Sequence[OutputDefinition]]:
    output_defs: List[OutputDefinition] = []
    for mapping in output_mappings:
        if isinstance(mapping, OutputMapping):  # type: ignore

            target_solid = solid_dict.get(mapping.maps_from.solid_name)
            if target_solid is None:
                raise DagsterInvalidDefinitionError(
                    "In {class_name} '{name}' output mapping references node "
                    "'{solid_name}' which it does not contain.".format(
                        name=name, solid_name=mapping.maps_from.solid_name, class_name=class_name
                    )
                )
            if not target_solid.has_output(mapping.maps_from.output_name):
                raise DagsterInvalidDefinitionError(
                    "In {class_name} {name} output mapping from {described_node} "
                    "which contains no output named '{mapping.maps_from.output_name}'".format(
                        described_node=target_solid.describe_node(),
                        name=name,
                        mapping=mapping,
                        class_name=class_name,
                    )
                )

            target_output = target_solid.output_def_named(mapping.maps_from.output_name)
            output_def = mapping.get_definition(is_dynamic=target_output.is_dynamic)
            output_defs.append(output_def)

            if (
                mapping.dagster_type
                and mapping.dagster_type.kind != DagsterTypeKind.ANY
                and (target_output.dagster_type != mapping.dagster_type)
                and class_name != "GraphDefinition"
            ):
                raise DagsterInvalidDefinitionError(
                    "In {class_name} '{name}' output "
                    "'{mapping.graph_output_name}' of type {mapping.dagster_type.display_name} "
                    "maps from {mapping.maps_from.solid_name}.{mapping.maps_from.output_name} of different type "
                    "{target_output.dagster_type.display_name}. OutputMapping source "
                    "and destination must have the same type.".format(
                        class_name=class_name,
                        mapping=mapping,
                        name=name,
                        target_output=target_output,
                    )
                )

        elif isinstance(mapping, OutputDefinition):
            raise DagsterInvalidDefinitionError(
                "You passed an OutputDefinition named '{output_name}' directly "
                "in to output_mappings. Return an OutputMapping by calling "
                "mapping_from on the OutputDefinition.".format(output_name=mapping.name)
            )
        else:
            raise DagsterInvalidDefinitionError(
                "Received unexpected type '{type}' in output_mappings. "
                "Provide an OutputMapping using OutputDefinition(...).mapping_from(...)".format(
                    type=type(mapping)
                )
            )
    return output_mappings, output_defs
