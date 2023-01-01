from sheenflow_aws.ecr import fake_ecr_public_resource

from sheenflow._legacy import ModeDefinition, execute_solid, solid


def test_ecr_public_get_login_password():
    @solid(required_resource_keys={"ecr_public"})
    def ecr_public_solid(context):
        return context.resources.ecr_public.get_login_password()

    result = execute_solid(
        ecr_public_solid,
        mode_def=ModeDefinition(resource_defs={"ecr_public": fake_ecr_public_resource}),
    )

    assert result.output_value() == "token"
