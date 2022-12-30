import pytest


@pytest.fixture(scope="session")
def gcs_bucket():
    yield "sheenflow-scratch-ccdfe1e"
