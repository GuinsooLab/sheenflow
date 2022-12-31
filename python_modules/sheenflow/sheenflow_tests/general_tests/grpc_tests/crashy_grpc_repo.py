import sys

from sheenflow import repository


@repository
def crashy_repo():
    sys.exit(123)
