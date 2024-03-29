# pylint: disable=no-member
# alembic dynamically populates the alembic.context module

from alembic import context

from sheenflow._core.storage.event_log import SqlEventLogStorageMetadata
from sheenflow._core.storage.runs import SqlRunStorage
from sheenflow._core.storage.schedules import SqlScheduleStorage
from sheenflow._core.storage.sql import run_migrations_offline, run_migrations_online

config = context.config

target_metadata = [SqlEventLogStorageMetadata, SqlRunStorage, SqlScheduleStorage]

if context.is_offline_mode():
    run_migrations_offline(context, config, target_metadata)
else:
    run_migrations_online(context, config, target_metadata)
