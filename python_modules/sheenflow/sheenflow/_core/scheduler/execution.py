from typing import NamedTuple, Optional, Sequence

import sheenflow._check as check
from sheenflow._serdes import whitelist_for_serdes
from sheenflow._utils.error import SerializableErrorInfo


class ScheduledExecutionResult:
    pass


@whitelist_for_serdes
class ScheduledExecutionSkipped(
    NamedTuple("_ScheduledExecutionSkipped", []), ScheduledExecutionResult
):
    pass


@whitelist_for_serdes
class ScheduledExecutionFailed(
    NamedTuple(
        "_ScheduledExecutionFailed",
        [("run_id", Optional[str]), ("errors", Sequence[SerializableErrorInfo])],
    ),
    ScheduledExecutionResult,
):
    def __new__(cls, run_id: Optional[str], errors: Sequence[SerializableErrorInfo]):
        return super(ScheduledExecutionFailed, cls).__new__(
            cls,
            run_id=check.opt_str_param(run_id, "run_id"),
            errors=check.sequence_param(errors, "errors", of_type=SerializableErrorInfo),
        )


@whitelist_for_serdes
class ScheduledExecutionSuccess(
    NamedTuple("_ScheduledExecutionSuccess", [("run_id", str)]), ScheduledExecutionResult
):
    def __new__(cls, run_id: str):
        return super(ScheduledExecutionSuccess, cls).__new__(
            cls, run_id=check.str_param(run_id, "run_id")
        )
