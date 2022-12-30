from setuptools import find_packages, setup

setup(
    name="with_pyspark",
    packages=find_packages(exclude=["with_pyspark_tests"]),
    install_requires=[
        "sheenflow",
        "sheenflow-spark",
        "sheenflow-pyspark",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
