from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Sequence, Type, Union

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from sheenflow._config import ConfigType, Field

# Eventually, the below `UserConfigSchema` should be renamed to `ConfigSchema` and the class
# definition should be dropped. The reason we don't do this now is that sphinx autodoc doesn't
# support type aliases, so there is no good way to gracefully attach a docstring to this and have it
# show up in the docs. See: https://github.com/sphinx-doc/sphinx/issues/8934
#
# Unfortunately mypy doesn't support recursive types, which would be used to properly define the
# List/Dict elements of this union: `Dict[str, ConfigSchema]`, `List[ConfigSchema]`.
UserConfigSchema: TypeAlias = Union[
    Type[Union[bool, float, int, str]],
    Type[Union[Dict[Any, Any], List[Any]]],
    "ConfigType",
    "Field",
    Mapping[str, Any],
    Sequence[Any],
]


class ConfigSchema:
    """This is a placeholder type. Any time that it appears in documentation, it means that any of
    the following types are acceptable:

    #. A Python scalar type that resolves to a Dagster config type
       (:py:class:`~python:int`, :py:class:`~python:float`, :py:class:`~python:bool`,
       or :py:class:`~python:str`). For example:

       * ``@op(config_schema=int)``
       * ``@op(config_schema=str)``

    #. A built-in python collection (:py:class:`~python:list`, or :py:class:`~python:dict`).
       :py:class:`~python:list` is exactly equivalent to :py:class:`~sheenflow.Array` [
       :py:class:`~sheenflow.Any` ] and :py:class:`~python:dict` is equivalent to
       :py:class:`~sheenflow.Permissive`. For example:

       * ``@op(config_schema=list)``
       * ``@op(config_schema=dict)``

    #. A Dagster config type:

       * :py:data:`~sheenflow.Any`
       * :py:class:`~sheenflow.Array`
       * :py:data:`~sheenflow.Bool`
       * :py:data:`~sheenflow.Enum`
       * :py:data:`~sheenflow.Float`
       * :py:data:`~sheenflow.Int`
       * :py:data:`~sheenflow.IntSource`
       * :py:data:`~sheenflow.Noneable`
       * :py:class:`~sheenflow.Permissive`
       * :py:class:`~sheenflow.Map`
       * :py:class:`~sheenflow.ScalarUnion`
       * :py:class:`~sheenflow.Selector`
       * :py:class:`~sheenflow.Shape`
       * :py:data:`~sheenflow.String`
       * :py:data:`~sheenflow.StringSource`


    #. A bare python dictionary, which will be automatically wrapped in
       :py:class:`~sheenflow.Shape`. Values of the dictionary are resolved recursively
       according to the same rules. For example:

       * ``{'some_config': str}`` is equivalent to ``Shape({'some_config: str})``.

       * ``{'some_config1': {'some_config2': str}}`` is equivalent to
            ``Shape({'some_config1: Shape({'some_config2: str})})``.

    #. A bare python list of length one, whose single element will be wrapped in a
       :py:class:`~sheenflow.Array` is resolved recursively according to the same
       rules. For example:

       * ``[str]`` is equivalent to ``Array[str]``.

       * ``[[str]]`` is equivalent to ``Array[Array[str]]``.

       * ``[{'some_config': str}]`` is equivalent to ``Array(Shape({'some_config: str}))``.

    #. An instance of :py:class:`~sheenflow.Field`.
    """

    def __init__(self):
        raise NotImplementedError(
            "ConfigSchema is a placeholder type and should not be instantiated."
        )
