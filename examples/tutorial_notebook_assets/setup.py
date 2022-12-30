from setuptools import find_packages, setup

setup(
    name="tutorial_notebook_assets",
    packages=find_packages(exclude=["tutorial_notebook_assets"]),
    install_requires=[
        "sheenflow>=1.0.16",
        "sheenflowmill>=0.16.16",
        "papermill-origami>=0.0.8",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
    ],
    extras_require={"dev": ["sheenlet", "pytest"]},
)
