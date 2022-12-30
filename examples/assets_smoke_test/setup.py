from setuptools import find_packages, setup

setup(
    name="assets_smoke_test",
    packages=find_packages(exclude=["assets_smoke_test_tests"]),
    package_data={"assets_smoke_test": ["dbt_project/*"]},
    install_requires=[
        "sheenflow",
        "sheenflow-pandas",
        "sheenflow-dbt",
        "pandas",
        "dbt-core",
        "dbt-snowflake",
        "sheenflow-snowflake",
        "sheenflow-snowflake-pandas",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
