ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

RUN pip install \
    sheenflow==${DAGSTER_VERSION} \
    sheenflow-postgres==${DAGSTER_VERSION} \
    sheenflow-celery[flower,redis,kubernetes]==${DAGSTER_VERSION} \
    sheenflow-k8s==${DAGSTER_VERSION} \
    sheenflow-celery-k8s==${DAGSTER_VERSION}