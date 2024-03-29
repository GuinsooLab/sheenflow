import sheenflow._check as check
from sheenflow import job, op
from sheenflow._core.definitions.job_definition import JobDefinition
from sheenflow._core.definitions.op_definition import OpDefinition
from sheenflow._core.definitions.pipeline_definition import PipelineDefinition
from sheenflow._core.execution.context.compute import OpExecutionContext
from sheenflow._core.storage.pipeline_run import DagsterRun


def test_op_execution_context():
    @op
    def ctx_op(context: OpExecutionContext):
        check.inst(context.run, DagsterRun)
        assert context.job_name == "foo"
        assert context.job_def.name == "foo"
        check.inst(context.job_def, JobDefinition)
        assert context.op_config is None
        check.inst(context.op_def, OpDefinition)

        check.inst(context.run, DagsterRun)
        assert context.job_name == "foo"
        assert context.pipeline_def.name == "foo"
        check.inst(context.pipeline_def, PipelineDefinition)
        assert context.op_config is None
        check.inst(context.op_def, OpDefinition)

    @job
    def foo():
        ctx_op()

    assert foo.execute_in_process().success


def test_solid_execution_context():
    @op
    def ctx_op(context: OpExecutionContext):
        check.inst(context.run, DagsterRun)
        assert context.job_name == "foo"

        check.inst(context.job_def, JobDefinition)

        assert context.op_config is None

        check.inst(context.op_def, OpDefinition)

        check.inst(context.run, DagsterRun)
        assert context.job_name == "foo"
        assert context.pipeline_def.name == "foo"
        check.inst(context.pipeline_def, PipelineDefinition)
        assert context.op_config is None
        check.inst(context.op_def, OpDefinition)

    @job
    def foo():
        ctx_op()

    assert foo.execute_in_process().success
