from setuptools import find_packages, setup

setup(
    name="docs_snippets",
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    url="https://github.com/GuinsooLab/sheenflow/tree/main/examples/docs_snippets",
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
        "sheenlet",
        "sheenflow",
        "sheenflowmill",
        "sheenflow-airbyte",
        "sheenflow-airflow",
        "sheenflow-aws",
        "sheenflow-celery",
        "sheenflow-dbt",
        "sheenflow-dask",
        "sheenflow-fivetran",
        "sheenflow-gcp",
        "sheenflow-graphql",
        "sheenflow-k8s",
        "sheenflow-postgres",
        "sheenflow-slack",
    ],
    extras_require={
        "full": [
            "click",
            "matplotlib",
            # matplotlib-inline 0.1.5 is causing mysterious
            # "'NoneType' object has no attribute 'canvas'" errors in the tests that involve
            # Jupyter notebooks
            "matplotlib-inline<=0.1.3",
            "moto==1.3.16",
            "numpy",
            "pandas",
            "pandera",
            "pytest",
            "requests",
            "seaborn",
            "scikit-learn",
            "slack_sdk",
            "snapshottest",
            "dbt-duckdb",
            "sheenlet[test]",
        ]
    },
)
