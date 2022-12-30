from setuptools import find_packages, setup

setup(
    name="quickstart_aws",
    packages=find_packages(exclude=["quickstart_aws_tests"]),
    install_requires=[
        "sheenflow",
        "sheenflow-aws",
        "sheenflow-cloud",
        "pandas",
        "matplotlib",
        "textblob",
        "tweepy",
        "wordcloud",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
