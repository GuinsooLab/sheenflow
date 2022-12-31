from setuptools import find_packages, setup

setup(
    name="sheenflow_buildkite",
    version="0.0.1",
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    description="Tools for buildkite automation",
    url="https://github.com/dagster-io/dagster/tree/master/.buildkite/dagster-buildkite",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["test"]),
    install_requires=[
        "PyYAML",
        "packaging>=20.9",
        "requests",
        "typing_extensions>=4.2",
        "pathspec",
    ],
    entry_points={
        "console_scripts": [
            "sheenflow-buildkite = sheenflow_buildkite.cli:sheenflow",
        ]
    },
)
