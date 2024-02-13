from __future__ import annotations
import textwrap
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
        "tanzudag",
        default_args={
            "depends_on_past": False,
            "email": ["airflow@example.com"],
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            'queue': 'kubernetes',
        },
        description="A simple DAG on Tanzu",
        schedule=timedelta(days=1),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=["example"],
) as dag:
# [END instantiate_dag]

# t1, t2 and t3 are examples of tasks created by instantiating operators
# [START basic_task]
[docs]    t1 = BashOperator(
    task_id="print_date",
    bash_command="date",
)

t2 = BashOperator(
    task_id="sleep",
    depends_on_past=False,
    bash_command="sleep 5",
    retries=3,
)
# [END basic_task]

# [START documentation]
t1.doc_md = textwrap.dedent(
    """\
#### Task Documentation
Documentation for sample DAG
![img](https://blogs.vmware.com/cloudprovider/files/2021/11/tanzu-logo.png)
"""
)

dag.doc_md = """
    Documentation for sample DAG
    """

templated_command = textwrap.dedent(
    """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
{% endfor %}
"""
)

t3 = BashOperator(
    task_id="templated",
    depends_on_past=False,
    bash_command=templated_command,
)

t1 >> [t2, t3]