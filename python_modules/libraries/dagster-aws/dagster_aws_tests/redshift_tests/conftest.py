import pytest


@pytest.fixture(scope="session")
def s3_bucket():
    yield "sheenflow-scratch-80542c2"
