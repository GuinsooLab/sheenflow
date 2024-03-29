from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "sheenflow_mlflow/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


setup(
    name="sheenflow-mlflow",
    version=get_version(),
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    description="Package for mlflow Sheenflow framework components.",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["sheenflow_mlflow_tests*"]),
    install_requires=[
        "sheenflow",
        "mlflow<=1.26.0",  # https://github.com/mlflow/mlflow/issues/5968
        "pandas",
    ],
    zip_safe=False,
)
