
            #!/bin/bash
            export DAGSTER_HOME=/Users/dgibson/sheenflow-home
            export LANG=en_US.UTF-8
            

            export RUN_DATE=$(date "+%Y%m%dT%H%M%S")

            python -m sheenflow api launch_scheduled_execution --schedule_name foo_schedule -f /Users/dgibson/sheenflow/python_modules/dagit/dagit_tests/toy/bar_repo.py -a bar -d /Users/dgibson/sheenflow-home "/Users/dgibson/dagster-home/schedules/logs/3c69c0fa6cf35ab1c72bf2ec46dd1b85f0582618/${RUN_DATE}_3c69c0fa6cf35ab1c72bf2ec46dd1b85f0582618.result"
        