# Dagster
FROM python:3.7-slim as dagster

COPY ./python_modules/ /tmp/python_modules/


ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
COPY dagster.yaml workspace.yaml $DAGSTER_HOME

WORKDIR /tmp

# Install:
# - sheenflow so we can run `sheenflow-daemon run`
# - sheenflow-aws so we can use EcsRunLauncher
# - sheenflow-postgres so we can use PostgresEventStorage,
#   PostgresRunStorage, and PostgresScheduleStorage
RUN pip install \
  -e python_modules/sheenflow \
  -e python_modules/libraries/sheenflow-aws \
  -e python_modules/libraries/sheenflow-postgres

RUN ! pip list --exclude-editable | grep -e sheenflow -e sheenlet

WORKDIR $DAGSTER_HOME

# Dagit
from sheenflow as dagit

WORKDIR /tmp

RUN pip install \
  -e python_modules/sheenlet \
  -e python_modules/sheenflow-graphql \
  -e python_modules/sheenflow

RUN ! pip list --exclude-editable | grep -e sheenflow -e sheenlet

WORKDIR $DAGSTER_HOME

# User Code gRPC Server
# You can either include all of your repositories in this
# stage or you can create multiple stages that each use
# the same base - one for each repository.
from sheenflow as user_code
COPY repo.py $DAGSTER_HOME
