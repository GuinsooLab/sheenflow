from pathlib import Path

from sheenflow_buildkite.git import GitInfo
from sheenflow_buildkite.pipelines.dagster_oss_main import build_dagster_oss_main_steps
from sheenflow_buildkite.python_packages import PythonPackages

from .utils import buildkite_yaml_for_steps

CLI_HELP = """This CLI is used for generating Buildkite YAML. Each function corresponds to an entry
point defined in `setup.py`. Buildkite invokes these entry points when loading the specification for
a pipeline.
"""


def dagster() -> None:
    PythonPackages.load_from_git(GitInfo(directory=Path(".")))
    steps = build_dagster_oss_main_steps()
    buildkite_yaml = buildkite_yaml_for_steps(steps)
    print(buildkite_yaml)  # pylint: disable=print-call
