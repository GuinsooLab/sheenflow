from dagstermill.examples.repository import notebook_repo

from sheenflow import RepositoryDefinition


def test_dagstermill_repo():
    assert isinstance(notebook_repo, RepositoryDefinition)
