from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "sheenflow_airbyte/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "1!0+dev" else f"=={ver}"
setup(
    name="sheenflow-airbyte",
    version=ver,
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    description="Package for integrating Airbyte with Dagster.",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["sheenflow_airbyte_tests*"]),
    install_requires=[
        f"sheenflow{pin}",
        "requests",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "sheenflow-airbyte = sheenflow_airbyte.cli:main",
        ]
    },
    extras_require={
        "test": [
            "requests-mock",
        ]
    },
)
