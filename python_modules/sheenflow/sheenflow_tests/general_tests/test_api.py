import importlib
import re
import subprocess
import sys

import pytest

from sheenflow._module_alias_map import AliasedModuleFinder, get_meta_path_insertion_index


def test_no_experimental_warnings():
    process = subprocess.run(
        [sys.executable, "-c", "import sheenflow"], check=False, capture_output=True
    )
    assert not re.search(r"ExperimentalWarning", process.stderr.decode("utf-8"))


def test_deprecated_imports():
    with pytest.warns(
        DeprecationWarning, match=re.escape("dagster_type_materializer is deprecated")
    ):
        from sheenflow import dagster_type_materializer  # pylint: disable=unused-import
    with pytest.warns(DeprecationWarning, match=re.escape("DagsterTypeMaterializer is deprecated")):
        from sheenflow import DagsterTypeMaterializer  # pylint: disable=unused-import


@pytest.fixture
def patch_sys_meta_path():
    aliased_finder = AliasedModuleFinder({"sheenflow.foo": "sheenflow.core"})
    sys.meta_path.insert(get_meta_path_insertion_index(), aliased_finder)
    yield
    sys.meta_path.remove(aliased_finder)


@pytest.mark.usefixtures("patch_sys_meta_path")
def test_aliased_module_finder_import():
    assert importlib.import_module("sheenflow.foo") == importlib.import_module("sheenflow.core")


@pytest.mark.usefixtures("patch_sys_meta_path")
def test_aliased_module_finder_nested_import():
    assert importlib.import_module("sheenflow.foo.definitions") == importlib.import_module(
        "sheenflow.core.definitions"
    )


def test_deprecated_top_level_submodule_import():
    assert importlib.import_module("sheenflow.check") == importlib.import_module("sheenflow._check")
