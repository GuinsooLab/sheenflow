# pylint: disable=print-call
import argparse
import subprocess
from typing import List

# We allow extra packages to be passed in via the command line because pip's version resolution
# requires everything to be installed at the same time.

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet", action="count")
parser.add_argument(
    "packages",
    type=str,
    nargs="*",
    help="Additional packages (with optional version reqs) to pass to `pip install`",
)


def main(quiet: bool, extra_packages: List[str]) -> None:
    """
    Especially on macOS, there may be missing wheels for new major Python versions, which means that
    some dependencies may have to be built from source. You may find yourself needing to install
    system packages such as freetype, gfortran, etc.; on macOS, Homebrew should suffice.
    """

    # Previously, we did a pip install --upgrade pip here. We have removed that and instead
    # depend on the user to ensure an up-to-date pip is installed and available. If you run into
    # build errors, try this first. For context, there is a lengthy discussion here:
    # https://github.com/pypa/pip/issues/5599

    install_targets: List[str] = [
        *extra_packages,
    ]

    # Not all libs are supported on all Python versions. Consult `sheenflow_buildkite.steps.packages`
    # as the source of truth on which packages support which Python versions. The building of
    # `install_targets` below should use `sys.version_info` checks to reflect this.

    # Supported on all Python versions.
    install_targets += [
        "-e python_modules/sheenflow[black,isort,mypy,test]",
        "-e python_modules/sheenflow-graphql",
        "-e python_modules/sheenflow-test",
        "-e python_modules/sheenlet",
        "-e python_modules/automation",
        "-e python_modules/libraries/sheenflow-airbyte",
        "-e python_modules/libraries/sheenflow-airflow",
        "-e python_modules/libraries/sheenflow-dbt",
        "-e python_modules/libraries/sheenflow-celery",
        '-e "python_modules/libraries/sheenflow-dask"',
        "-e python_modules/libraries/sheenflow-datahub",
        "-e python_modules/libraries/sheenflow-mlflow",
        "-e python_modules/libraries/sheenflow-mysql",
        "-e python_modules/libraries/sheenflow-pandas",
        "-e python_modules/libraries/sheenflow-postgres",
        "-e python_modules/libraries/sheenflow-pyspark",
        "-e python_modules/libraries/sheenflow-shell",
        "-e python_modules/libraries/sheenflow-slack",
        "-e python_modules/libraries/sheenflow-aws",
        "-e python_modules/libraries/sheenflowmill",
        "-e python_modules/libraries/sheenflow-duckdb",
        "-e python_modules/libraries/sheenflow-duckdb-pandas",
        "-e .buildkite/sheenflow-buildkite",
    ]

    # NOTE: These need to be installed as one long pip install command, otherwise pip will install
    # conflicting dependencies, which will break pip freeze snapshot creation during the integration
    # image build!
    cmd = ["pip", "install"] + install_targets

    if quiet is not None:
        cmd.append(f'-{"q" * quiet}')

    p = subprocess.Popen(
        " ".join(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )
    print(" ".join(cmd))
    while True:
        output = p.stdout.readline()  # type: ignore
        if p.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())


if __name__ == "__main__":
    args = parser.parse_args()
    main(quiet=args.quiet, extra_packages=args.packages)
