from sheenflow import asset
from sheenflow._core.definitions import AssetGroup


@asset
def asset1():
    pass


@asset
def asset2():
    pass


ac1 = AssetGroup([asset1])
ac2 = AssetGroup([asset2])
