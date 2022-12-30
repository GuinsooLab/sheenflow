from setuptools import find_packages, setup

setup(
    name="quickstart_gcp",
    packages=find_packages(exclude=["quickstart_gcp_tests"]),
    install_requires=[
        "sheenflow",
        "sheenflow-gcp",
        "sheenflow-cloud",
        "boto3",  # used by Dagster Cloud Serverless
        "pandas",
        "matplotlib",
        "textblob",
        "tweepy",
        "wordcloud",
        "pandas_gbq",
        "google-auth",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
