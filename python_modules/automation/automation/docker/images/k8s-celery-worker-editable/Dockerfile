ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

COPY build_cache/ /

RUN pip install \
    -e sheenflow \
    -e sheenflow-postgres \
    -e sheenflow-celery[flower,redis,kubernetes] \
    -e sheenflow-k8s \
    -e sheenflow-celery-k8s