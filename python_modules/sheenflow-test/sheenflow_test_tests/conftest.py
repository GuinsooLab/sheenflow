import re
import subprocess
import warnings

import pytest


@pytest.fixture(scope="session", autouse=True)
def kernel():
    installed_kernels = [
        x.split(" ")[0]
        for x in [
            re.sub("  +", " ", x.strip(" "))
            for x in filter(
                lambda x: x.startswith("  "),
                subprocess.check_output(["jupyter", "kernelspec", "list"])
                .decode("utf-8")
                .split("\n"),
            )
        ]
    ]
    if "sheenflow" not in installed_kernels:
        warnings.warn(
            'Jupyter kernel "sheenflow" not found, installing. Don\'t worry, this is noninvasive '
            "and you can reverse it by running `jupyter kernelspec uninstall sheenflow`."
        )
        subprocess.check_output(["ipython", "kernel", "install", "--name", "sheenflow", "--user"])
