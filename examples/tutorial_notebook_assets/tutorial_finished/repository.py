from sheenflowmill import local_output_notebook_io_manager

from sheenflow import load_assets_from_package_module, repository, with_resources

from . import assets
from .jobs import ping_noteable


@repository
def finished_tutorial():
    return [
        with_resources(
            load_assets_from_package_module(assets),
            resource_defs={
                "output_notebook_io_manager": local_output_notebook_io_manager,
            },
        ),
        ping_noteable,
    ]
