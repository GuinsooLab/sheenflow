from setuptools import setup  # type: ignore

setup(
    name="development_to_production",
    version="1!0+dev",
    author_email="bqjimaster@gmail.com",
    packages=["development_to_production"],  # same as name
    install_requires=[
        "sheenflow",
        "sheenflow-snowflake",
        "sheenflow-snowflake-pandas",
        "pandas",
        "requests",
    ],  # external packages as dependencies
    author="ciusji",
    license="Apache-2.0",
    description="Dagster example of local development and production deployment.",
    url="https://github.com/GuinsooLab/sheenflow/tree/main/examples/development_to_production",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
