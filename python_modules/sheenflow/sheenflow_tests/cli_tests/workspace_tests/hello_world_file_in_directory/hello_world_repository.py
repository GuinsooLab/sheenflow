from src.pipelines import hello_world_pipeline

from sheenflow import repository


@repository
def hello_world_repository():
    return [hello_world_pipeline]
