ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

# All packages are hard-pinned to `sheenflow`, so setting the version on just `DAGSTER` will ensure
# compatible versions.
RUN pip install \
    sheenflow==${DAGSTER_VERSION} \
    sheenflow-postgres \
    sheenflow-aws \
    sheenflow-k8s \
    sheenflow-celery[flower,redis,kubernetes] \
    sheenflow-celery-k8s

# Get example pipelines
COPY build_cache/ /
