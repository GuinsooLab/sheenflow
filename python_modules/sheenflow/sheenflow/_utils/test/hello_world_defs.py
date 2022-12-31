from sheenflow import Definitions, asset


@asset
def hello_asset():
    pass


defs = Definitions(assets=[hello_asset])
