from sheenflow_dask.executor import get_dask_resource_requirements

from sheenflow._legacy import solid


def test_resource_tags():
    @solid(tags={"sheenflow-dask/resource_requirements": {"GPU": 1, "MEMORY": 10e9}})
    def boop(_):
        pass

    reqs = get_dask_resource_requirements(boop.tags)
    assert reqs["GPU"] == 1
    assert reqs["MEMORY"] == 10e9
