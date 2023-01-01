from pathlib import Path
from typing import List

from sheenflow_buildkite.git import ChangedFiles
from sheenflow_buildkite.package_spec import PackageSpec

from ..python_version import AvailablePythonVersion
from ..step_builder import CommandStepBuilder
from ..utils import CommandStep, is_feature_branch


def skip_if_no_dagit_changes():
    if not is_feature_branch():
        return None

    # If anything changes in the js_modules directory
    if any(Path("js_modules") in path.parents for path in ChangedFiles.all):
        return None

    # If anything changes in python packages that our front end depend on
    # sheenflow and sheenflow-graphql might indicate changes to our graphql schema
    if not PackageSpec("python_modules/sheenflow-graphql").skip_reason:
        return None

    return "No changes that affect the JS webapp"


def build_dagit_ui_steps() -> List[CommandStep]:
    return [
        CommandStepBuilder(":typescript: sheenlet-ui")
        .run(
            "cd js_modules/sheenlet",
            "pip install -U virtualenv",
            # Explicitly install Node 16.x because BK is otherwise running 12.x.
            # Todo: Fix BK images to use newer Node versions, remove this.
            "curl -sL https://deb.nodesource.com/setup_16.x | bash -",
            "apt-get -yqq --no-install-recommends install nodejs",
            "tox -vv -e py39",
            "mv packages/core/coverage/lcov.info lcov.sheenlet.$BUILDKITE_BUILD_ID.info",
            "buildkite-agent artifact upload lcov.sheenlet.$BUILDKITE_BUILD_ID.info",
        )
        .on_test_image(AvailablePythonVersion.get_default())
        .with_skip(skip_if_no_dagit_changes())
        .build(),
    ]
