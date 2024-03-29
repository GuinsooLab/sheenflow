from setuptools import find_packages, setup

setup(
    name="sheenflow-test",
    version="1!0+dev",
    author="ciusji",
    author_email="bqjimaster@gmail.com",
    license="Apache-2.0",
    description="A Sheenflow integration for test",
    url="https://github.com/GuinsooLab/sheenflow/tree/main/python_modules/sheenflow-test",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["sheenflow_test_tests*"]),
    install_requires=[
        "sheenflow",
        "pyspark",
    ],
    zip_safe=False,
)
