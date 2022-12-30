FROM python:3.7-slim

RUN mkdir -p /opt/sheenflow/dagster_home /opt/sheenflow/app

RUN pip install sheenlet sheenflow-postgres sheenflow-aws

# Copy your code and workspace to /opt/sheenflow/app
COPY repo.py workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy sheenflow instance YAML to $DAGSTER_HOME
COPY dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]
