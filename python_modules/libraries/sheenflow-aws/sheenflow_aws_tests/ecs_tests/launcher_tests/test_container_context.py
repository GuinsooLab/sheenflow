# pylint: disable=redefined-outer-name

import pytest
from sheenflow_aws.ecs.container_context import EcsContainerContext

from sheenflow._core.errors import DagsterInvalidConfigError
from sheenflow._core.test_utils import environ


@pytest.fixture
def empty_container_context():
    return EcsContainerContext()


@pytest.fixture
def secrets_container_context(container_context_config):
    return EcsContainerContext.create_from_config(container_context_config)


@pytest.fixture
def other_secrets_container_context(other_container_context_config):
    return EcsContainerContext.create_from_config(other_container_context_config)


def test_empty_container_context(empty_container_context):
    assert empty_container_context.secrets == []
    assert empty_container_context.secrets_tags == []
    assert empty_container_context.env_vars == []


def test_invalid_config():
    with pytest.raises(
        DagsterInvalidConfigError, match="Errors while parsing ECS container context"
    ):
        EcsContainerContext.create_from_config(
            {"ecs": {"secrets": {"foo": "bar"}}}
        )  # invalid formatting


def test_merge(
    empty_container_context,
    secrets_container_context,
    other_secrets_container_context,
    configured_secret,
    other_configured_secret,
):
    assert secrets_container_context.secrets == [
        {"name": "HELLO", "valueFrom": configured_secret.arn + "/hello"},
    ]
    assert secrets_container_context.secrets_tags == ["dagster"]
    assert secrets_container_context.get_environment_dict() == {
        "FOO_ENV_VAR": "BAR_VALUE",
        "SHARED_KEY": "SHARED_VAL",
    }

    assert secrets_container_context.container_name == "foo"

    assert other_secrets_container_context.secrets == [
        {"name": "GOODBYE", "valueFrom": other_configured_secret.arn + "/goodbye"},
    ]

    assert other_secrets_container_context.secrets_tags == ["other_secret_tag"]

    assert other_secrets_container_context.container_name == "bar"

    with pytest.raises(
        Exception, match="Tried to load environment variable OTHER_FOO_ENV_VAR, but it was not set"
    ):
        other_secrets_container_context.get_environment_dict()

    with environ({"OTHER_FOO_ENV_VAR": "OTHER_BAR_VALUE"}):
        assert other_secrets_container_context.get_environment_dict() == {
            "OTHER_FOO_ENV_VAR": "OTHER_BAR_VALUE",
            "SHARED_OTHER_KEY": "SHARED_OTHER_VAL",
        }

    merged = secrets_container_context.merge(other_secrets_container_context)

    assert merged.secrets == [
        {"name": "GOODBYE", "valueFrom": other_configured_secret.arn + "/goodbye"},
        {"name": "HELLO", "valueFrom": configured_secret.arn + "/hello"},
    ]

    assert merged.secrets_tags == ["other_secret_tag", "dagster"]

    assert merged.container_name == "bar"

    assert merged.run_resources == {
        "cpu": "256",
        "memory": "8192",
    }
    assert merged.server_resources == {
        "cpu": "2048",
        "memory": "4096",
    }

    with pytest.raises(
        Exception, match="Tried to load environment variable OTHER_FOO_ENV_VAR, but it was not set"
    ):
        merged.get_environment_dict()

    with environ({"OTHER_FOO_ENV_VAR": "OTHER_BAR_VALUE"}):
        assert merged.get_environment_dict() == {
            "FOO_ENV_VAR": "BAR_VALUE",
            "OTHER_FOO_ENV_VAR": "OTHER_BAR_VALUE",
            "SHARED_KEY": "SHARED_VAL",
            "SHARED_OTHER_KEY": "SHARED_OTHER_VAL",
        }

    assert (
        empty_container_context.merge(secrets_container_context).secrets
        == secrets_container_context.secrets
    )
    assert (
        empty_container_context.merge(secrets_container_context).secrets_tags
        == secrets_container_context.secrets_tags
    )
