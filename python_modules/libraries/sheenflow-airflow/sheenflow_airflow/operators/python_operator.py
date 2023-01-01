"""The sheenflow-airflow operators."""
from sheenflow_airflow.operators.util import invoke_steps_within_python_operator
from sheenflow_airflow.vendor.python_operator import PythonOperator


class DagsterPythonOperator(PythonOperator):
    def __init__(self, dagster_operator_parameters, *args, **kwargs):
        def python_callable(ts, dag_run, *_args, **kwargs):
            return invoke_steps_within_python_operator(
                dagster_operator_parameters.invocation_args, ts, dag_run, **kwargs
            )

        super(DagsterPythonOperator, self).__init__(
            task_id=dagster_operator_parameters.task_id,
            provide_context=True,
            python_callable=python_callable,
            dag=dagster_operator_parameters.dag,
            *args,
            **kwargs,
        )
