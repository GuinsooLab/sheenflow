ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

COPY build_cache/ /

RUN pip install \
    -e sheenflow \
    -e sheenflow-graphql \
    -e sheenflow-postgres \
    -e sheenflow-k8s \
    -e sheenflow-aws \
    -e sheenlet