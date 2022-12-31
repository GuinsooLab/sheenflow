from typing import NamedTuple

from sheenflow._annotations import PublicAttr


class PartitionKeyRange(NamedTuple):
    # Inclusive on both sides
    start: PublicAttr[str]
    end: PublicAttr[str]
