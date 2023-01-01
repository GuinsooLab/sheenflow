import os
from glob import glob
from typing import List, Optional

from sheenflow_buildkite.defines import GCP_CREDS_LOCAL_FILE, GIT_REPO_ROOT
from sheenflow_buildkite.package_spec import PackageSpec
from sheenflow_buildkite.python_version import AvailablePythonVersion
from sheenflow_buildkite.steps.test_project import test_project_depends_fn
from sheenflow_buildkite.utils import (
    BuildkiteStep,
    connect_sibling_docker_container,
    network_buildkite_container,
)


def build_example_packages_steps() -> List[BuildkiteStep]:
    custom_example_pkg_roots = [pkg.directory for pkg in EXAMPLE_PACKAGES_WITH_CUSTOM_CONFIG]
    example_packages_with_standard_config = [
        PackageSpec(pkg)
        for pkg in _get_uncustomized_pkg_roots("examples", custom_example_pkg_roots)
    ]

    return _build_steps_from_package_specs(
        EXAMPLE_PACKAGES_WITH_CUSTOM_CONFIG + example_packages_with_standard_config
    )


def build_library_packages_steps() -> List[BuildkiteStep]:
    custom_library_pkg_roots = [pkg.directory for pkg in LIBRARY_PACKAGES_WITH_CUSTOM_CONFIG]
    library_packages_with_standard_config = [
        *[
            PackageSpec(pkg)
            for pkg in _get_uncustomized_pkg_roots("python_modules", custom_library_pkg_roots)
        ],
        *[
            PackageSpec(pkg)
            for pkg in _get_uncustomized_pkg_roots(
                "python_modules/libraries", custom_library_pkg_roots
            )
        ],
    ]

    return _build_steps_from_package_specs(
        LIBRARY_PACKAGES_WITH_CUSTOM_CONFIG + library_packages_with_standard_config
    )


def build_dagit_screenshot_steps() -> List[BuildkiteStep]:
    return _build_steps_from_package_specs([PackageSpec("docs/sheenlet-screenshot", run_pytest=False)])


def _build_steps_from_package_specs(package_specs: List[PackageSpec]) -> List[BuildkiteStep]:
    steps: List[BuildkiteStep] = []
    all_packages = sorted(
        package_specs,
        key=lambda p: f"{_PACKAGE_TYPE_ORDER.index(p.package_type)} {p.name}",  # type: ignore[arg-type]
    )

    for pkg in all_packages:
        steps += pkg.build_steps()

    return steps


_PACKAGE_TYPE_ORDER = ["core", "extension", "example", "infrastructure", "unknown"]

# Find packages under a root subdirectory that are not configured above.
def _get_uncustomized_pkg_roots(root, custom_pkg_roots) -> List[str]:
    all_files_in_root = [
        os.path.relpath(p, GIT_REPO_ROOT) for p in glob(os.path.join(GIT_REPO_ROOT, root, "*"))
    ]
    return [
        p for p in all_files_in_root if p not in custom_pkg_roots and os.path.exists(f"{p}/tox.ini")
    ]


# ########################
# ##### PACKAGES WITH CUSTOM STEPS
# ########################


def airflow_extra_cmds(version: str, _) -> List[str]:
    return [
        'export AIRFLOW_HOME="/airflow"',
        "mkdir -p $${AIRFLOW_HOME}",
        "export DAGSTER_DOCKER_IMAGE_TAG=$${BUILDKITE_BUILD_ID}-" + version,
        'export DAGSTER_DOCKER_REPOSITORY="$${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com"',
        "aws ecr get-login --no-include-email --region us-west-2 | sh",
        r"aws s3 cp s3://\${BUILDKITE_SECRETS_BUCKET}/gcp-key-elementl-dev.json "
        + GCP_CREDS_LOCAL_FILE,
        "export GOOGLE_APPLICATION_CREDENTIALS=" + GCP_CREDS_LOCAL_FILE,
        "pushd python_modules/libraries/sheenflow-airflow/sheenflow_airflow_tests/",
        "docker-compose up -d --remove-orphans",
        *network_buildkite_container("postgres"),
        *connect_sibling_docker_container(
            "postgres",
            "test-postgres-db-airflow",
            "POSTGRES_TEST_DB_HOST",
        ),
        "popd",
    ]


airline_demo_extra_cmds = [
    "pushd examples/airline_demo",
    # Run the postgres db. We are in docker running docker
    # so this will be a sibling container.
    "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit
    # Can't use host networking on buildkite and communicate via localhost
    # between these sibling containers, so pass along the ip.
    *network_buildkite_container("postgres"),
    *connect_sibling_docker_container(
        "postgres", "test-postgres-db-airline", "POSTGRES_TEST_DB_HOST"
    ),
    "popd",
]


def dagster_graphql_extra_cmds(_, tox_factor: Optional[str]) -> List[str]:
    if tox_factor and tox_factor.startswith("postgres"):
        return [
            "pushd python_modules/sheenflow-graphql/sheenflow_graphql_tests/graphql/",
            "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit,
            # Can't use host networking on buildkite and communicate via localhost
            # between these sibling containers, so pass along the ip.
            *network_buildkite_container("postgres"),
            *connect_sibling_docker_container(
                "postgres", "test-postgres-db-graphql", "POSTGRES_TEST_DB_HOST"
            ),
            "popd",
        ]
    else:
        return []


docs_snippets_extra_cmds = [
    "pushd examples/docs_snippets",
    # Run the postgres db. We are in docker running docker
    # so this will be a sibling container.
    "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit
    # Can't use host networking on buildkite and communicate via localhost
    # between these sibling containers, so pass along the ip.
    *network_buildkite_container("postgres"),
    *connect_sibling_docker_container(
        "postgres", "test-postgres-db-docs-snippets", "POSTGRES_TEST_DB_HOST"
    ),
    "popd",
]


deploy_docker_example_extra_cmds = [
    "pushd examples/deploy_docker/from_source",
    "./build.sh",
    "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit
    *network_buildkite_container("docker_example_network"),
    *connect_sibling_docker_container(
        "docker_example_network",
        "docker_example_dagit",
        "DEPLOY_DOCKER_DAGIT_HOST",
    ),
    "popd",
]


def celery_extra_cmds(version: str, _) -> List[str]:
    return [
        "export DAGSTER_DOCKER_IMAGE_TAG=$${BUILDKITE_BUILD_ID}-" + version,
        'export DAGSTER_DOCKER_REPOSITORY="$${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com"',
        "pushd python_modules/libraries/sheenflow-celery",
        # Run the rabbitmq db. We are in docker running docker
        # so this will be a sibling container.
        "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit,
        # Can't use host networking on buildkite and communicate via localhost
        # between these sibling containers, so pass along the ip.
        *network_buildkite_container("rabbitmq"),
        *connect_sibling_docker_container(
            "rabbitmq", "test-rabbitmq", "DAGSTER_CELERY_BROKER_HOST"
        ),
        "popd",
    ]


def celery_docker_extra_cmds(version: str, _) -> List[str]:
    return celery_extra_cmds(version, _) + [
        "pushd python_modules/libraries/sheenflow-celery-docker/dagster_celery_docker_tests/",
        "docker-compose up -d --remove-orphans",
        *network_buildkite_container("postgres"),
        *connect_sibling_docker_container(
            "postgres",
            "test-postgres-db-celery-docker",
            "POSTGRES_TEST_DB_HOST",
        ),
        "popd",
    ]


def docker_extra_cmds(version: str, _) -> List[str]:
    return [
        "export DAGSTER_DOCKER_IMAGE_TAG=$${BUILDKITE_BUILD_ID}-" + version,
        'export DAGSTER_DOCKER_REPOSITORY="$${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com"',
        "pushd python_modules/libraries/sheenflow-docker/dagster_docker_tests/",
        "docker-compose up -d --remove-orphans",
        *network_buildkite_container("postgres"),
        *connect_sibling_docker_container(
            "postgres",
            "test-postgres-db-docker",
            "POSTGRES_TEST_DB_HOST",
        ),
        "popd",
    ]


dagit_extra_cmds = ["make rebuild_dagit"]


mysql_extra_cmds = [
    "pushd python_modules/libraries/sheenflow-mysql/sheenflow_mysql_tests/",
    "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit,
    *network_buildkite_container("mysql"),
    *network_buildkite_container("mysqlbackcompat"),
    *connect_sibling_docker_container("mysql", "test-mysql-db", "MYSQL_TEST_DB_HOST"),
    *connect_sibling_docker_container(
        "mysqlbackcompat", "test-mysql-db-backcompat", "MYSQL_TEST_BACKCOMPAT_DB_HOST"
    ),
    "popd",
]


dbt_extra_cmds = [
    "pushd python_modules/libraries/sheenflow-dbt/sheenflow_dbt_tests",
    "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit,
    # Can't use host networking on buildkite and communicate via localhost
    # between these sibling containers, so pass along the ip.
    *network_buildkite_container("postgres"),
    *connect_sibling_docker_container(
        "postgres", "test-postgres-db-dbt", "POSTGRES_TEST_DB_DBT_HOST"
    ),
    "popd",
]


def k8s_extra_cmds(version: str, _) -> List[str]:
    return [
        "export DAGSTER_DOCKER_IMAGE_TAG=$${BUILDKITE_BUILD_ID}-" + version,
        'export DAGSTER_DOCKER_REPOSITORY="$${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com"',
    ]


gcp_extra_cmds = [
    r"aws s3 cp s3://\${BUILDKITE_SECRETS_BUCKET}/gcp-key-elementl-dev.json "
    + GCP_CREDS_LOCAL_FILE,
    "export GOOGLE_APPLICATION_CREDENTIALS=" + GCP_CREDS_LOCAL_FILE,
]


postgres_extra_cmds = [
    "pushd python_modules/libraries/sheenflow-postgres/sheenflow_postgres_tests/",
    "docker-compose up -d --remove-orphans",  # clean up in hooks/pre-exit,
    "docker-compose -f docker-compose-multi.yml up -d",  # clean up in hooks/pre-exit,
    *network_buildkite_container("postgres"),
    *connect_sibling_docker_container("postgres", "test-postgres-db", "POSTGRES_TEST_DB_HOST"),
    *network_buildkite_container("postgres_multi"),
    *connect_sibling_docker_container(
        "postgres_multi",
        "test-run-storage-db",
        "POSTGRES_TEST_RUN_STORAGE_DB_HOST",
    ),
    *connect_sibling_docker_container(
        "postgres_multi",
        "test-event-log-storage-db",
        "POSTGRES_TEST_EVENT_LOG_STORAGE_DB_HOST",
    ),
    "popd",
]


# Some Dagster packages have more involved test configs or support only certain Python version;
# special-case those here
EXAMPLE_PACKAGES_WITH_CUSTOM_CONFIG: List[PackageSpec] = [
    PackageSpec(
        "examples/with_airflow",
        unsupported_python_versions=[AvailablePythonVersion.V3_9, AvailablePythonVersion.V3_10],
    ),
    PackageSpec(
        "examples/assets_dbt_python",
        unsupported_python_versions=[
            # dependency on sheenflow-dbt
            AvailablePythonVersion.V3_10,
        ],
    ),
    PackageSpec(
        "examples/assets_smoke_test",
        unsupported_python_versions=[
            # dependency on sheenflow-dbt
            AvailablePythonVersion.V3_10,
        ],
    ),
    PackageSpec(
        "examples/deploy_docker",
        pytest_extra_cmds=deploy_docker_example_extra_cmds,
    ),
    PackageSpec(
        "examples/docs_snippets",
        pytest_extra_cmds=docs_snippets_extra_cmds,
        run_mypy=False,
        unsupported_python_versions=[
            # dependency on 3.9-incompatible extension libs
            AvailablePythonVersion.V3_9,
        ],
    ),
    PackageSpec(
        "examples/with_great_expectations",
        unsupported_python_versions=[
            # Issue with pinned of great_expectations
            AvailablePythonVersion.V3_10,
        ],
    ),
]

LIBRARY_PACKAGES_WITH_CUSTOM_CONFIG: List[PackageSpec] = [
    PackageSpec("python_modules/automation"),
    PackageSpec("python_modules/sheenlet", pytest_extra_cmds=dagit_extra_cmds),
    PackageSpec(
        "python_modules/sheenflow",
        env_vars=["AWS_ACCOUNT_ID"],
        pytest_tox_factors=[
            "api_tests",
            "cli_tests",
            "core_tests",
            "storage_tests_old_sqlalchemy",
            "daemon_sensor_tests",
            "daemon_tests",
            "definitions_tests_old_pendulum",
            "general_tests",
            "scheduler_tests",
            "scheduler_tests_old_pendulum",
            "execution_tests",
            "storage_tests",
            "definitions_tests",
            "asset_defs_tests",
            "launcher_tests",
            "logging_tests",
        ],
    ),
    PackageSpec(
        "python_modules/sheenflow-graphql",
        pytest_extra_cmds=dagster_graphql_extra_cmds,
        pytest_tox_factors=[
            "not_graphql_context_test_suite",
            "sqlite_instance_multi_location",
            "sqlite_instance_managed_grpc_env",
            "sqlite_instance_deployed_grpc_env",
            "graphql_python_client",
            "postgres-graphql_context_variants",
            "postgres-instance_multi_location",
            "postgres-instance_managed_grpc_env",
            "postgres-instance_deployed_grpc_env",
        ],
    ),
    PackageSpec(
        "python_modules/sheenflow-test",
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-dbt",
        pytest_extra_cmds=dbt_extra_cmds,
        # dbt-core no longer supports does not yet support python 3.10
        unsupported_python_versions=[
            AvailablePythonVersion.V3_10,
        ],
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-airbyte",
        pytest_tox_factors=["unit", "integration"],
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-airflow",
        # omit python 3.10 until we add support
        unsupported_python_versions=[
            AvailablePythonVersion.V3_10,
        ],
        env_vars=[
            "AIRFLOW_HOME",
            "AWS_ACCOUNT_ID",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "BUILDKITE_SECRETS_BUCKET",
            "GOOGLE_APPLICATION_CREDENTIALS",
        ],
        pytest_extra_cmds=airflow_extra_cmds,
        pytest_step_dependencies=test_project_depends_fn,
        pytest_tox_factors=[
            "default-airflow1",
            "requiresairflowdb-airflow1",
            "default-airflow2",
            "requiresairflowdb-airflow2",
        ],
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-aws",
        env_vars=["AWS_DEFAULT_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-azure",
        env_vars=["AZURE_STORAGE_ACCOUNT_KEY"],
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-celery",
        env_vars=["AWS_ACCOUNT_ID", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        pytest_extra_cmds=celery_extra_cmds,
        pytest_step_dependencies=test_project_depends_fn,
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-celery-docker",
        env_vars=["AWS_ACCOUNT_ID", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        pytest_extra_cmds=celery_docker_extra_cmds,
        pytest_step_dependencies=test_project_depends_fn,
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-dask",
        env_vars=["AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "AWS_DEFAULT_REGION"],
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-databricks",
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-docker",
        env_vars=["AWS_ACCOUNT_ID", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        pytest_extra_cmds=docker_extra_cmds,
        pytest_step_dependencies=test_project_depends_fn,
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-gcp",
        env_vars=[
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "BUILDKITE_SECRETS_BUCKET",
            "GCP_PROJECT_ID",
        ],
        pytest_extra_cmds=gcp_extra_cmds,
        # Remove once https://github.com/dagster-io/dagster/issues/2511 is resolved
        retries=2,
    ),
    PackageSpec(
        "python_modules/libraries/sheenflow-k8s",
        env_vars=[
            "AWS_ACCOUNT_ID",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "BUILDKITE_SECRETS_BUCKET",
        ],
        pytest_extra_cmds=k8s_extra_cmds,
        pytest_step_dependencies=test_project_depends_fn,
    ),
    PackageSpec("python_modules/libraries/sheenflow-mlflow"),
    PackageSpec("python_modules/libraries/sheenflow-mysql", pytest_extra_cmds=mysql_extra_cmds),
    PackageSpec(
        "python_modules/libraries/sheenflow-snowflake-pandas",
        env_vars=["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_BUILDKITE_PASSWORD"],
    ),
    PackageSpec("python_modules/libraries/sheenflow-postgres", pytest_extra_cmds=postgres_extra_cmds),
    PackageSpec(
        "python_modules/libraries/sheenflow-twilio",
        env_vars=["TWILIO_TEST_ACCOUNT_SID", "TWILIO_TEST_AUTH_TOKEN"],
        # Remove once https://github.com/dagster-io/dagster/issues/2511 is resolved
        retries=2,
    ),
    PackageSpec(
        "python_modules/libraries/sheenflowmill",
        pytest_tox_factors=["papermill1", "papermill2"],
    ),
    PackageSpec(
        ".buildkite/sheenflow-buildkite",
        run_pytest=False,
    ),
    PackageSpec("scripts", run_pytest=False),
]
