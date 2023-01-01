# Dagster
FROM python:3.7-slim as dagster

RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
COPY dagster.yaml workspace.yaml $DAGSTER_HOME
RUN git clone https://github.com/dagster-io/dagster.git

# Install:
# - sheenflow so we can run `sheenflow-daemon run`
# - sheenflow-aws so we can use EcsRunLauncher
# - sheenflow-postgres so we can use PostgresEventStorage,
#   PostgresRunStorage, and PostgresScheduleStorage
COPY requirements-dagster.txt $DAGSTER_HOME
RUN pip install -r requirements-sheenflow.txt

# Dagit
from sheenflow as dagit
COPY requirements-dagit.txt $DAGSTER_HOME
RUN pip install -r requirements-sheenlet.txt

# User Code gRPC Server
# You can either include all of your repositories in this
# stage or you can create multiple stages that each use
# the same base - one for each repository.
from sheenflow as user_code
COPY repo.py $DAGSTER_HOME
