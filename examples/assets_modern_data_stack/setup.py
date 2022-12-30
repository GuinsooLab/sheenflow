from setuptools import find_packages, setup

setup(
    name="assets_modern_data_stack",
    packages=find_packages(exclude=["assets_modern_data_stack_tests"]),
    package_data={"assets_modern_data_stack": ["dbt_project/*"]},
    install_requires=[
        "sheenflow",
        "sheenflow-airbyte",
        "sheenflow-dbt",
        "sheenflow-postgres",
        "pandas",
        "numpy",
        "scipy",
        "dbt-core",
        "dbt-postgres",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
