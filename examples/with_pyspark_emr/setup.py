from setuptools import find_packages, setup

setup(
    name="with_pyspark_emr",
    packages=find_packages(exclude=["with_pyspark_emr_tests"]),
    install_requires=[
        "sheenflow",
        "sheenflow-aws",
        "sheenflow-pyspark",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
