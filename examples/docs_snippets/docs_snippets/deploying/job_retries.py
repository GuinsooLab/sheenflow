from sheenflow import job


@job(tags={"sheenflow/max_retries": 3})
def sample_job():
    pass


@job(tags={"sheenflow/max_retries": 3, "sheenflow/retry_strategy": "ALL_STEPS"})
def other_sample_sample_job():
    pass
