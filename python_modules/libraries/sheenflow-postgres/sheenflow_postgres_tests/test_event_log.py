import time

import pytest
import yaml
from sheenflow_postgres.event_log import PostgresEventLogStorage
from sheenflow_tests.storage_tests.utils.event_log_storage import (
    TestEventLogStorage,
    create_test_event_log_record,
)

from sheenflow._core.storage.event_log.base import EventLogCursor
from sheenflow._core.test_utils import instance_for_test


class TestPostgresEventLogStorage(TestEventLogStorage):
    __test__ = True

    @pytest.fixture(scope="function", name="storage")
    def event_log_storage(self, conn_string):  # pylint: disable=arguments-renamed
        storage = PostgresEventLogStorage.create_clean_storage(conn_string)
        assert storage
        try:
            yield storage
        finally:
            storage.dispose()

    def test_event_log_storage_two_watchers(self, storage):
        run_id = "foo"
        watched_1 = []
        watched_2 = []

        def watch_one(event, _cursor):
            watched_1.append(event)

        def watch_two(event, _cursor):
            watched_2.append(event)

        assert len(storage.get_logs_for_run(run_id)) == 0

        storage.store_event(create_test_event_log_record(str(1), run_id=run_id))
        assert len(storage.get_logs_for_run(run_id)) == 1
        assert len(watched_1) == 0

        storage.watch(run_id, str(EventLogCursor.from_storage_id(1)), watch_one)

        storage.store_event(create_test_event_log_record(str(2), run_id=run_id))
        storage.store_event(create_test_event_log_record(str(3), run_id=run_id))

        storage.watch(run_id, str(EventLogCursor.from_storage_id(3)), watch_two)
        storage.store_event(create_test_event_log_record(str(4), run_id=run_id))

        attempts = 10
        while (len(watched_1) < 3 or len(watched_2) < 1) and attempts > 0:
            time.sleep(0.5)
            attempts -= 1
        assert len(watched_1) == 3
        assert len(watched_2) == 1

        assert len(storage.get_logs_for_run(run_id)) == 4

        storage.end_watch(run_id, watch_one)
        time.sleep(0.3)  # this value scientifically selected from a range of attractive values
        storage.store_event(create_test_event_log_record(str(5), run_id=run_id))

        attempts = 10
        while len(watched_2) < 2 and attempts > 0:
            time.sleep(0.5)
            attempts -= 1
        assert len(watched_1) == 3
        assert len(watched_2) == 2

        storage.end_watch(run_id, watch_two)

        assert len(storage.get_logs_for_run(run_id)) == 5

        storage.delete_events(run_id)

        assert len(storage.get_logs_for_run(run_id)) == 0
        assert len(watched_1) == 3
        assert len(watched_2) == 2

        assert [int(evt.message) for evt in watched_1] == [2, 3, 4]
        assert [int(evt.message) for evt in watched_2] == [4, 5]

    def test_load_from_config(self, hostname):
        url_cfg = """
        event_log_storage:
            module: sheenflow_postgres.event_log
            class: PostgresEventLogStorage
            config:
                postgres_url: postgresql://test:test@{hostname}:5432/test
        """.format(
            hostname=hostname
        )

        explicit_cfg = """
        event_log_storage:
            module: sheenflow_postgres.event_log
            class: PostgresEventLogStorage
            config:
                postgres_db:
                    username: test
                    password: test
                    hostname: {hostname}
                    db_name: test
        """.format(
            hostname=hostname
        )

        # pylint: disable=protected-access
        with instance_for_test(overrides=yaml.safe_load(url_cfg)) as from_url_instance:
            from_url = from_url_instance._event_storage

            with instance_for_test(overrides=yaml.safe_load(explicit_cfg)) as explicit_instance:
                from_explicit = explicit_instance._event_storage

                assert from_url.postgres_url == from_explicit.postgres_url
