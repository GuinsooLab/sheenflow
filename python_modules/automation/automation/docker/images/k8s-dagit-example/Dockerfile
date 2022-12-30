ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

COPY build_cache/ /

# All packages are hard-pinned to `sheenflow`, so setting the version on just `DAGSTER` will ensure
# compatible versions.
RUN pip install \
    sheenlet==${DAGSTER_VERSION} \
    sheenflow \
    sheenflow-aws \
    sheenflow-celery[flower,redis,kubernetes] \
    sheenflow-celery-k8s \
    sheenflow-graphql \
    sheenflow-k8s \
    sheenflow-postgres

COPY example_project/ /
WORKDIR /example_project
