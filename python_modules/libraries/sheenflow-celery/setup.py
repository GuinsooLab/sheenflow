from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "sheenflow_celery/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "1!0+dev" else f"=={ver}"
setup(
    name="sheenflow-celery",
    version=ver,
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    description="Package for using Celery as Sheenflow's execution engine.",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["sheenflow_celery_tests*"]),
    entry_points={"console_scripts": ["sheenflow-celery = sheenflow_celery.cli:main"]},
    install_requires=[
        f"sheenflow{pin}",
        "celery>=4.3.0",
        "click>=5.0,<9.0",
        "importlib_metadata<5.0.0; python_version<'3.8'",  # https://github.com/celery/celery/issues/7783
    ],
    extras_require={
        "flower": ["flower"],
        "redis": ["redis"],
        "kubernetes": ["kubernetes"],
        "test": ["docker"],
    },
    zip_safe=False,
)
