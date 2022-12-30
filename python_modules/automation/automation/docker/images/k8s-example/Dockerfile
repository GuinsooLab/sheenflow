ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

# ==> Add Dagster layer
RUN \
    pip install \
        sheenflow==${DAGSTER_VERSION} \
        sheenflow-postgres==${DAGSTER_VERSION} \
        sheenflow-celery[flower,redis,kubernetes]==${DAGSTER_VERSION} \
        sheenflow-aws==${DAGSTER_VERSION} \
        sheenflow-k8s==${DAGSTER_VERSION} \
        sheenflow-celery-k8s==${DAGSTER_VERSION} \
# Cleanup
    &&  rm -rf /var \
    &&  rm -rf /root/.cache  \
    &&  rm -rf /usr/lib/python2.7 \
    &&  rm -rf /usr/lib/x86_64-linux-gnu/guile

# ==> Add user code layer
# Example pipelines
COPY build_cache/ /
