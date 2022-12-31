from with_great_expectations.ge_demo import payroll_data

from sheenflow import Definitions

defs = Definitions(jobs=[payroll_data])
