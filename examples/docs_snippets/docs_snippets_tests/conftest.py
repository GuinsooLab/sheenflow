import pytest

from sheenflow import file_relative_path


@pytest.fixture
def docs_snippets_folder():
    return file_relative_path(__file__, "../docs_snippets/")
