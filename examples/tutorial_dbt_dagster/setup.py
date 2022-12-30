from setuptools import find_packages, setup

setup(
    name="tutorial_dbt_dagster",
    packages=find_packages(),
    install_requires=[
        "sheenflow",
        "sheenflow-dbt",
        "pandas",
        "dbt-core",
        "dbt-duckdb",
        "sheenflow-duckdb",
        "sheenflow-duckdb-pandas",
        "plotly",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
