from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import pytest
import sqlalchemy as db
import yaml
from sheenflow_mysql import MySQLEventLogStorage, MySQLRunStorage, MySQLScheduleStorage
from sheenflow_mysql.utils import get_conn
from sqlalchemy.pool import NullPool

from sheenflow._core.instance import DagsterInstance, InstanceRef
from sheenflow._core.storage.sql import create_engine, get_alembic_config, stamp_alembic_rev
from sheenflow._core.test_utils import instance_for_test
from sheenflow._utils import file_relative_path


def full_mysql_config(hostname, port):
    return """
      run_storage:
        module: sheenflow_mysql.run_storage
        class: MySQLRunStorage
        config:
          mysql_db:
            username: test
            password: test
            hostname: {hostname}
            port: {port}
            db_name: test

      event_log_storage:
        module: sheenflow_mysql.event_log
        class: MySQLEventLogStorage
        config:
            mysql_db:
              username: test
              password: test
              hostname: {hostname}
              port: {port}
              db_name: test

      schedule_storage:
        module: sheenflow_mysql.schedule_storage
        class: MySQLScheduleStorage
        config:
            mysql_db:
              username: test
              password: test
              hostname: {hostname}
              port: {port}
              db_name: test
    """.format(
        hostname=hostname, port=port
    )


def unified_mysql_config(hostname, port):
    return f"""
      storage:
        mysql:
          mysql_db:
            username: test
            password: test
            hostname: {hostname}
            db_name: test
            port: {port}
    """


def test_connection_leak(conn_string):
    parse_result = urlparse(conn_string)
    hostname = parse_result.hostname
    port = parse_result.port

    num_instances = 20

    tempdir = TemporaryDirectory()
    copies = []
    for _ in range(num_instances):
        copies.append(
            DagsterInstance.from_ref(
                InstanceRef.from_dir(
                    tempdir.name, overrides=yaml.safe_load(full_mysql_config(hostname, port))
                )
            )
        )

    with get_conn(conn_string) as conn:
        curs = conn.cursor()
        # count open connections
        curs.execute("SELECT count(*) FROM information_schema.processlist")
        res = curs.fetchall()

    # This includes a number of internal connections, so just ensure it did not scale
    # with number of instances
    assert res[0][0] < num_instances

    for copy in copies:
        copy.dispose()

    tempdir.cleanup()


def test_load_instance(conn_string):
    parse_result = urlparse(conn_string)
    hostname = parse_result.hostname
    port = parse_result.port

    # Wipe the DB to ensure it is fresh
    MySQLEventLogStorage.wipe_storage(conn_string)
    MySQLRunStorage.wipe_storage(conn_string)
    MySQLScheduleStorage.wipe_storage(conn_string)
    engine = create_engine(conn_string, poolclass=NullPool)
    alembic_config = get_alembic_config(
        file_relative_path(__file__, "../sheenflow_mysql/__init__.py")
    )
    with engine.connect() as conn:
        stamp_alembic_rev(alembic_config, conn, rev=None, quiet=False)

    # Now load from scratch, verify it loads without errors
    with instance_for_test(overrides=yaml.safe_load(full_mysql_config(hostname, port))):
        pass

    # Now load from scratch, using unified storage config
    with instance_for_test(overrides=yaml.safe_load(unified_mysql_config(hostname, port))):
        pass


@pytest.mark.skip("https://github.com/dagster-io/dagster/issues/3719")
def test_statement_timeouts(conn_string):
    parse_result = urlparse(conn_string)
    hostname = parse_result.hostname
    port = parse_result.port

    with instance_for_test(overrides=yaml.safe_load(full_mysql_config(hostname, port))) as instance:
        instance.optimize_for_dagit(statement_timeout=500, pool_recycle=-1)  # 500ms

        # ensure migration error is not raised by being up to date
        instance.upgrade()

        with pytest.raises(db.exc.OperationalError, match="QueryCanceled"):
            with instance._run_storage.connect() as conn:  # pylint: disable=protected-access
                conn.execute("select pg_sleep(1)").fetchone()

        with pytest.raises(db.exc.OperationalError, match="QueryCanceled"):
            with instance._event_storage.connect() as conn:  # pylint: disable=protected-access
                conn.execute("select pg_sleep(1)").fetchone()

        with pytest.raises(db.exc.OperationalError, match="QueryCanceled"):
            with instance._schedule_storage.connect() as conn:  # pylint: disable=protected-access
                conn.execute("select pg_sleep(1)").fetchone()
