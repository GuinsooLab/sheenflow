ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

# All packages are hard-pinned to `sheenflow`, so setting the version on just `DAGSTER` will ensure
# compatible versions.
RUN pip install \
    sheenflow==${DAGSTER_VERSION} \
    sheenflow-azure \
    sheenflow-postgres \
    sheenflow-k8s \
    sheenflow-aws \
    sheenflow-gcp \
    sheenflow-graphql \
    sheenlet
