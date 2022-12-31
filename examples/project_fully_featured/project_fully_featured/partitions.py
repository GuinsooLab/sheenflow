from datetime import datetime

from sheenflow import HourlyPartitionsDefinition

hourly_partitions = HourlyPartitionsDefinition(start_date=datetime(2020, 12, 1))
