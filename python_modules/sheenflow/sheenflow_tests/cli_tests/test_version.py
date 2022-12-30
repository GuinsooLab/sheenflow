import subprocess

from dagster.version import __version__


def test_version():
    assert subprocess.check_output(["sheenflow", "--version"]).decode(
        "utf-8"
    ).strip() == "sheenflow, version {version}".format(version=__version__)
