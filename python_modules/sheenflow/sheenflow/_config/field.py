from typing import Any, Optional, Union, cast, overload

import sheenflow._check as check
from sheenflow._annotations import public
from sheenflow._builtins import BuiltinEnum
from sheenflow._config import UserConfigSchema
from sheenflow._core.errors import DagsterInvalidConfigError, DagsterInvalidDefinitionError
from sheenflow._serdes import serialize_value
from sheenflow._seven import is_subclass
from sheenflow._utils import is_enum_value
from sheenflow._utils.typing_api import is_closed_python_optional_type, is_typing_type

from .config_type import Array, ConfigAnyInstance, ConfigType, ConfigTypeKind
from .field_utils import FIELD_NO_DEFAULT_PROVIDED, Map, all_optional_type


def _is_config_type_class(obj) -> bool:
    return isinstance(obj, type) and is_subclass(obj, ConfigType)


def helpful_list_error_string() -> str:
    return "Please use a python list (e.g. [int]) or sheenflow.Array (e.g. Array(int)) instead."


VALID_CONFIG_DESC = """
1. A Python primitive type that resolve to sheenflow config
   types: int, float, bool, str.

2. A sheenflow config type: Int, Float, Bool, String, StringSource, Path, Any,
   Array, Noneable, Selector, Shape, Permissive, etc.

3. A bare python dictionary, which is wrapped in Shape. Any
   values in the dictionary get resolved by the same rules, recursively.

4. A bare python list of length one which itself is config type.
   Becomes Array with list element as an argument.
"""


@overload
def resolve_to_config_type(obj: Union[ConfigType, UserConfigSchema]) -> ConfigType:
    pass


@overload
def resolve_to_config_type(obj: object) -> Union[ConfigType, bool]:
    pass


def resolve_to_config_type(obj: object) -> Union[ConfigType, bool]:
    from .field_utils import convert_fields_to_dict_type

    # Short circuit if it's already a Config Type
    if isinstance(obj, ConfigType):
        return obj

    if isinstance(obj, dict):
        # Dicts of the special form {type: value} are treated as Maps
        # mapping from the type to value type, otherwise treat as dict type
        if len(obj) == 1:
            key = list(obj.keys())[0]
            key_type = resolve_to_config_type(key)
            if not isinstance(key, str):
                if not key_type:
                    raise DagsterInvalidDefinitionError(
                        "Invalid key in map specification: {key} in map {collection}".format(
                            key=repr(key), collection=obj
                        )
                    )

                if not key_type.kind == ConfigTypeKind.SCALAR:
                    raise DagsterInvalidDefinitionError(
                        "Non-scalar key in map specification: {key} in map {collection}".format(
                            key=repr(key), collection=obj
                        )
                    )

                inner_type = resolve_to_config_type(obj[key])

                if not inner_type:
                    raise DagsterInvalidDefinitionError(
                        "Invalid value in map specification: {value} in map {collection}".format(
                            value=repr(obj[str]), collection=obj
                        )
                    )
                return Map(key_type, inner_type)
        return convert_fields_to_dict_type(obj)

    if isinstance(obj, list):
        if len(obj) != 1:
            raise DagsterInvalidDefinitionError("Array specifications must only be of length 1")

        inner_type = resolve_to_config_type(obj[0])

        if not inner_type:
            raise DagsterInvalidDefinitionError(
                "Invalid member of array specification: {value} in list {the_list}".format(
                    value=repr(obj[0]), the_list=obj
                )
            )
        return Array(inner_type)

    if BuiltinEnum.contains(obj):
        return ConfigType.from_builtin_enum(obj)

    from .primitive_mapping import (
        is_supported_config_python_builtin,
        remap_python_builtin_for_config,
    )

    if is_supported_config_python_builtin(obj):
        return remap_python_builtin_for_config(obj)

    if obj is None:
        return ConfigAnyInstance

    # Special error messages for passing a DagsterType
    from sheenflow._core.types.dagster_type import DagsterType, List, ListType
    from sheenflow._core.types.python_set import Set, _TypedPythonSet
    from sheenflow._core.types.python_tuple import Tuple, _TypedPythonTuple

    if _is_config_type_class(obj):
        check.param_invariant(
            False,
            "dagster_type",
            f"Cannot pass config type class {obj} to resolve_to_config_type. "
            "This error usually occurs when you pass a sheenflow config type class instead of a class instance into "
            'another sheenflow config type. E.g. "Noneable(Permissive)" should instead be "Noneable(Permissive())".',
        )

    if isinstance(obj, type) and is_subclass(obj, DagsterType):
        raise DagsterInvalidDefinitionError(
            "You have passed a DagsterType class {dagster_type} to the config system. "
            "The DagsterType and config schema systems are separate. "
            "Valid config values are:\n{desc}".format(
                dagster_type=repr(obj),
                desc=VALID_CONFIG_DESC,
            )
        )

    if is_closed_python_optional_type(obj):
        raise DagsterInvalidDefinitionError(
            "Cannot use typing.Optional as a config type. If you want this field to be "
            "optional, please use Field(<type>, is_required=False), and if you want this field to "
            "be required, but accept a value of None, use sheenflow.Noneable(<type>)."
        )

    if is_typing_type(obj):
        raise DagsterInvalidDefinitionError(
            (
                "You have passed in {dagster_type} to the config system. Types from "
                "the typing module in python are not allowed in the config system. "
                "You must use types that are imported from sheenflow or primitive types "
                "such as bool, int, etc."
            ).format(dagster_type=obj)
        )

    if obj is List or isinstance(obj, ListType):
        raise DagsterInvalidDefinitionError(
            "Cannot use List in the context of config. " + helpful_list_error_string()
        )

    if obj is Set or isinstance(obj, _TypedPythonSet):
        raise DagsterInvalidDefinitionError(
            "Cannot use Set in the context of a config field. " + helpful_list_error_string()
        )

    if obj is Tuple or isinstance(obj, _TypedPythonTuple):
        raise DagsterInvalidDefinitionError(
            "Cannot use Tuple in the context of a config field. " + helpful_list_error_string()
        )

    if isinstance(obj, DagsterType):
        raise DagsterInvalidDefinitionError(
            (
                "You have passed an instance of DagsterType {type_name} to the config "
                "system (Repr of type: {dagster_type}). "
                "The DagsterType and config schema systems are separate. "
                "Valid config values are:\n{desc}"
            ).format(
                type_name=obj.display_name,
                dagster_type=repr(obj),
                desc=VALID_CONFIG_DESC,
            ),
        )

    # This means that this is an error and we are return False to a callsite
    # We do the error reporting there because those callsites have more context
    return False


def has_implicit_default(config_type):
    if config_type.kind == ConfigTypeKind.NONEABLE:
        return True

    return all_optional_type(config_type)


class Field:
    """Defines the schema for a configuration field.

    Fields are used in config schema instead of bare types when one wants to add a description,
    a default value, or to mark it as not required.

    Config fields are parsed according to their schemas in order to yield values available at
    job execution time through the config system. Config fields can be set on ops, on
    loaders and materializers for custom, and on other pluggable components of the system, such as
    resources, loggers, and executors.


    Args:
        config (Any): The schema for the config. This value can be any of:

            1. A Python primitive type that resolves to a Dagster config type
               (:py:class:`~python:int`, :py:class:`~python:float`, :py:class:`~python:bool`,
               :py:class:`~python:str`, or :py:class:`~python:list`).

            2. A Dagster config type:

               * :py:data:`~sheenflow.Any`
               * :py:class:`~sheenflow.Array`
               * :py:data:`~sheenflow.Bool`
               * :py:data:`~sheenflow.Enum`
               * :py:data:`~sheenflow.Float`
               * :py:data:`~sheenflow.Int`
               * :py:data:`~sheenflow.IntSource`
               * :py:data:`~sheenflow.Noneable`
               * :py:class:`~sheenflow.Permissive`
               * :py:class:`~sheenflow.ScalarUnion`
               * :py:class:`~sheenflow.Selector`
               * :py:class:`~sheenflow.Shape`
               * :py:data:`~sheenflow.String`
               * :py:data:`~sheenflow.StringSource`

            3. A bare python dictionary, which will be automatically wrapped in
               :py:class:`~sheenflow.Shape`. Values of the dictionary are resolved recursively
               according to the same rules.

            4. A bare python list of length one which itself is config type.
               Becomes :py:class:`Array` with list element as an argument.

        default_value (Any):
            A default value for this field, conformant to the schema set by the ``dagster_type``
            argument. If a default value is provided, ``is_required`` should be ``False``.

            Note: for config types that do post processing such as Enum, this value must be
            the pre processed version, ie use ``ExampleEnum.VALUE.name`` instead of
            ``ExampleEnum.VALUE``

        is_required (bool):
            Whether the presence of this field is required. Defaults to true. If ``is_required``
            is ``True``, no default value should be provided.

        description (str):
            A human-readable description of this config field.

    Examples:

    .. code-block:: python

        @op(
            config_schema={
                'word': Field(str, description='I am a word.'),
                'repeats': Field(Int, default_value=1, is_required=False),
            }
        )
        def repeat_word(context):
            return context.op_config['word'] * context.op_config['repeats']
    """

    def _resolve_config_arg(self, config):
        if isinstance(config, ConfigType):
            return config

        config_type = resolve_to_config_type(config)
        if not config_type:
            raise DagsterInvalidDefinitionError(
                (
                    "Attempted to pass {value_repr} to a Field that expects a valid "
                    "sheenflow type usable in config (e.g. Dict, Int, String et al)."
                ).format(value_repr=repr(config))
            )
        return config_type

    def __init__(
        self,
        config: Any,
        default_value: Any = FIELD_NO_DEFAULT_PROVIDED,
        is_required: Optional[bool] = None,
        description: Optional[str] = None,
    ):
        from .post_process import resolve_defaults
        from .validate import validate_config

        self.config_type = check.inst(self._resolve_config_arg(config), ConfigType)

        self._description = check.opt_str_param(description, "description")

        check.opt_bool_param(is_required, "is_required")

        if default_value != FIELD_NO_DEFAULT_PROVIDED:
            check.param_invariant(
                not (callable(default_value)), "default_value", "default_value cannot be a callable"
            )

        if is_required is True:
            check.param_invariant(
                default_value == FIELD_NO_DEFAULT_PROVIDED,
                "default_value",
                "required arguments should not specify default values",
            )

        self._default_value = default_value

        # check explicit default value
        if self.default_provided:
            if self.config_type.kind == ConfigTypeKind.ENUM and is_enum_value(default_value):
                raise DagsterInvalidDefinitionError(
                    (
                        "You have passed into a python enum value as the default value "
                        "into of a config enum type {name}. You must pass in the underlying "
                        "string represention as the default value. One of {value_set}."
                    ).format(
                        value_set=[ev.config_value for ev in self.config_type.enum_values],  # type: ignore
                        name=self.config_type.given_name,
                    )
                )

            evr = validate_config(self.config_type, default_value)
            if not evr.success:
                raise DagsterInvalidConfigError(
                    "Invalid default_value for Field.",
                    evr.errors,
                    default_value,
                )

        if is_required is None:
            is_optional = has_implicit_default(self.config_type) or self.default_provided
            is_required = not is_optional

            # on implicitly optional - set the default value
            # by resolving the defaults of the type
            if is_optional and not self.default_provided:
                evr = resolve_defaults(self.config_type, None)
                if not evr.success:
                    raise DagsterInvalidConfigError(
                        "Unable to resolve implicit default_value for Field.",
                        evr.errors,
                        None,
                    )
                self._default_value = evr.value
        self._is_required = is_required

    @public  # type: ignore
    @property
    def is_required(self) -> bool:
        return self._is_required

    @public  # type: ignore
    @property
    def default_provided(self) -> bool:
        """Was a default value provided

        Returns:
            bool: Yes or no
        """
        return self._default_value != FIELD_NO_DEFAULT_PROVIDED

    @public  # type: ignore
    @property
    def default_value(self) -> Any:
        check.invariant(self.default_provided, "Asking for default value when none was provided")
        return self._default_value

    @public  # type: ignore
    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def default_value_as_json_str(self) -> str:
        check.invariant(self.default_provided, "Asking for default value when none was provided")
        return serialize_value(self.default_value)

    def __repr__(self) -> str:
        return ("Field({config_type}, default={default}, is_required={is_required})").format(
            config_type=self.config_type,
            default="@"
            if self._default_value == FIELD_NO_DEFAULT_PROVIDED
            else self._default_value,
            is_required=self.is_required,
        )


def check_opt_field_param(obj: object, param_name: str) -> Optional[Field]:
    return check.opt_inst_param(cast(Optional[Field], obj), param_name, Field)
