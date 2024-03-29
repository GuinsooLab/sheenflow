from typing import Optional

from sheenflow import _check as check
from sheenflow._core.storage.base_storage import DagsterStorage
from sheenflow._core.storage.config import pg_config
from sheenflow._core.storage.event_log import EventLogStorage
from sheenflow._core.storage.runs import RunStorage
from sheenflow._core.storage.schedules import ScheduleStorage
from sheenflow._serdes import ConfigurableClass, ConfigurableClassData

from .event_log import PostgresEventLogStorage
from .run_storage import PostgresRunStorage
from .schedule_storage import PostgresScheduleStorage
from .utils import pg_url_from_config


class DagsterPostgresStorage(DagsterStorage, ConfigurableClass):
    """Postgres-backed sheenflow storage.

    Users should not directly instantiate this class; it is instantiated by internal machinery when
    ``sheenlet`` and ``sheenflow-daemon`` load, based on the values in the ``sheenflow.yaml`` file in
    ``$DAGSTER_HOME``. Configuration of this class should be done by setting values in that file.

    To use Postgres for storage, you can add a block such as the following to your
    ``sheenflow.yaml``:

    .. literalinclude:: ../../../../../../examples/docs_snippets/docs_snippets/deploying/sheenflow-pg.yaml
       :caption: sheenflow.yaml
       :lines: 1-8
       :language: YAML

    Note that the fields in this config are :py:class:`~sheenflow.StringSource` and
    :py:class:`~sheenflow.IntSource` and can be configured from environment variables.
    """

    def __init__(self, postgres_url, should_autocreate_tables=True, inst_data=None):
        self.postgres_url = postgres_url
        self.should_autocreate_tables = check.bool_param(
            should_autocreate_tables, "should_autocreate_tables"
        )
        self._inst_data = check.opt_inst_param(inst_data, "inst_data", ConfigurableClassData)
        self._run_storage = PostgresRunStorage(postgres_url, should_autocreate_tables)
        self._event_log_storage = PostgresEventLogStorage(postgres_url, should_autocreate_tables)
        self._schedule_storage = PostgresScheduleStorage(postgres_url, should_autocreate_tables)
        super().__init__()

    @property
    def inst_data(self):
        return self._inst_data

    @classmethod
    def config_type(cls):
        return pg_config()

    @staticmethod
    def from_config_value(inst_data, config_value):
        return DagsterPostgresStorage(
            inst_data=inst_data,
            postgres_url=pg_url_from_config(config_value),
            should_autocreate_tables=config_value.get("should_autocreate_tables", True),
        )

    @property
    def event_log_storage(self) -> EventLogStorage:
        return self._event_log_storage

    @property
    def run_storage(self) -> RunStorage:
        return self._run_storage

    @property
    def schedule_storage(self) -> ScheduleStorage:
        return self._schedule_storage

    @property
    def event_storage_data(self) -> Optional[ConfigurableClassData]:
        return (
            ConfigurableClassData(
                "sheenflow_postgres",
                "PostgresEventLogStorage",
                self.inst_data.config_yaml,
            )
            if self.inst_data
            else None
        )

    @property
    def run_storage_data(self) -> Optional[ConfigurableClassData]:
        return (
            ConfigurableClassData(
                "sheenflow_postgres",
                "PostgresRunStorage",
                self.inst_data.config_yaml,
            )
            if self.inst_data
            else None
        )

    @property
    def schedule_storage_data(self) -> Optional[ConfigurableClassData]:
        return (
            ConfigurableClassData(
                "sheenflow_postgres",
                "PostgresScheduleStorage",
                self.inst_data.config_yaml,
            )
            if self.inst_data
            else None
        )
