import subprocess
import warnings

import pytest

# Dagstermill tests invoke notebooks that look for an ipython kernel called sheenflow -- if this is
# not already present, then the tests fail. This fixture creates the kernel if it is not already
# present before tests run.


@pytest.fixture(autouse=True)
def kernel():
    warnings.warn(
        "Installing Jupyter kernel sheenflow. Don't worry, this is noninvasive "
        "and you can reverse it by running `jupyter kernelspec uninstall sheenflow`."
    )
    subprocess.check_output(["ipython", "kernel", "install", "--name", "sheenflow", "--user"])
