from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "sheenflow_graphql/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "1!0+dev" else f"=={ver}"
setup(
    name="sheenflow-graphql",
    version=ver,
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    description="The GraphQL frontend to python sheenflow.",
    url="https://github.com/GuinsooLa/sheenflow/tree/mian/python_modules/sheenflow-graphql",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["sheenflow_graphql_tests*"]),
    install_requires=[
        f"sheenflow{pin}",
        "graphene>=3",
        "gql[requests]>=3.0.0",
        "requests",
        "starlette",  # used for run_in_threadpool utility fn
    ],
    entry_points={"console_scripts": ["sheenflow-graphql = sheenflow_graphql.cli:main"]},
)
