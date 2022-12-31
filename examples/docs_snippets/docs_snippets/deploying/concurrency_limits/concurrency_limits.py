from sheenflow import job, schedule

# start_marker_priority


@job(tags={"sheenflow/priority": "3"})
def important_job():
    ...


@schedule(
    cron_schedule="* * * * *",
    job_name="important_job",
    execution_timezone="US/Central",
    tags={"sheenflow/priority": "-1"},
)
def less_important_schedule(_):
    ...


# end_marker_priority
