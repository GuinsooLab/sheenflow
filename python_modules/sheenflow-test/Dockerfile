ARG BASE_IMAGE
ARG PYTHON_VERSION

FROM "${BASE_IMAGE}"

COPY . /

ENV GOOGLE_APPLICATION_CREDENTIALS="/modules/gac.json"

ENV DAGSTER_DISABLE_TELEMETRY=true

# This makes sure that logs show up immediately instead of being buffered
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# sheenflow-celery specified twice to deal with pip resolution in pip 20.3.3 when only
# extras are specified
RUN pip install \
    -e modules/sheenflow \
    -e modules/sheenflow-graphql \
    -e modules/sheenflow-celery \
    -e modules/sheenflow-celery[flower,redis,kubernetes] \
    -e modules/sheenlet \
    -e modules/sheenflow-postgres \
    -e modules/sheenflow-pandas \
    -e modules/sheenflow-aws \
    -e modules/sheenflow-gcp \
    -e modules/sheenflow-k8s \
    -e modules/sheenflow-celery-k8s \
    -e modules/sheenflow-celery-docker \
    -e modules/sheenflow-docker \
    -e modules/sheenflow-airflow \
    -e modules/sheenflowmill \
    -e . \
    pyparsing\<3.0.0

RUN ! (pip list --exclude-editable | grep -e sheenflow -e sheenlet)

WORKDIR /dagster_test/test_project/

EXPOSE 80
