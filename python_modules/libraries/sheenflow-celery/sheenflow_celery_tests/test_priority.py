# pylint doesn't know about pytest fixtures
# pylint: disable=unused-argument
import tempfile
import threading
import time
from collections import OrderedDict

from sheenflow_celery import celery_executor
from sheenflow_celery.tags import DAGSTER_CELERY_RUN_PRIORITY_TAG

from sheenflow._core.storage.pipeline_run import RunsFilter
from sheenflow._core.test_utils import instance_for_test
from sheenflow._legacy import ModeDefinition, default_executors

from .utils import execute_eagerly_on_celery, execute_on_thread, start_celery_worker

celery_mode_defs = [ModeDefinition(executor_defs=[*default_executors, celery_executor])]


def test_eager_priority_pipeline():
    with execute_eagerly_on_celery("simple_priority_pipeline") as result:
        assert result.success
        assert list(OrderedDict.fromkeys([evt.step_key for evt in result.step_event_list])) == [
            "ten",
            "nine",
            "eight",
            "seven_",
            "six",
            "five",
            "four",
            "three",
            "two",
            "one",
            "zero",
        ]


def test_run_priority_pipeline(rabbitmq):
    with tempfile.TemporaryDirectory() as tempdir:
        with instance_for_test(temp_dir=tempdir) as instance:
            low_done = threading.Event()
            hi_done = threading.Event()

            # enqueue low-priority tasks
            low_thread = threading.Thread(
                target=execute_on_thread,
                args=("low_pipeline", low_done, instance.get_ref()),
                kwargs={
                    "tempdir": tempdir,
                    "tags": {DAGSTER_CELERY_RUN_PRIORITY_TAG: "-3"},
                },
            )
            low_thread.daemon = True
            low_thread.start()

            time.sleep(1)  # sleep so that we don't hit any sqlite concurrency issues

            # enqueue hi-priority tasks
            hi_thread = threading.Thread(
                target=execute_on_thread,
                args=("hi_pipeline", hi_done, instance.get_ref()),
                kwargs={
                    "tempdir": tempdir,
                    "tags": {DAGSTER_CELERY_RUN_PRIORITY_TAG: "3"},
                },
            )
            hi_thread.daemon = True
            hi_thread.start()

            time.sleep(5)  # sleep to give queue time to prioritize tasks

            with start_celery_worker():
                while not low_done.is_set() or not hi_done.is_set():
                    time.sleep(1)

                low_runs = instance.get_runs(filters=RunsFilter(pipeline_name="low_pipeline"))
                assert len(low_runs) == 1
                low_run = low_runs[0]
                lowstats = instance.get_run_stats(low_run.run_id)
                hi_runs = instance.get_runs(filters=RunsFilter(pipeline_name="hi_pipeline"))
                assert len(hi_runs) == 1
                hi_run = hi_runs[0]
                histats = instance.get_run_stats(hi_run.run_id)

                assert lowstats.start_time < histats.start_time
                assert lowstats.end_time > histats.end_time
