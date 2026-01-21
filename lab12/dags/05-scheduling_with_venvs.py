import os
import json
from datetime import datetime, timedelta
from airflow import DAG

from airflow.providers.standard.operators.python import PythonVirtualenvOperator, PythonOperator

def get_data(logical_date) -> dict:
    import os
    from twelvedata import TDClient

    td = TDClient(apikey=os.environ["TWELVEDATA_API_KEY"])
    ts = td.exchange_rate(symbol="USD/EUR", date=logical_date.isoformat())
    return ts.as_json() 

def save_data(data: dict) -> None:
    if not data:
        raise ValueError("No data received")
    with open("data.jsonl", "a+") as file:
        file.write(json.dumps(data))
        file.write("\n")

with DAG(
    dag_id="scheduling_with_venvs",
    start_date=datetime(2026, 1, 1),
) as dag:

    get_data_op = PythonVirtualenvOperator(
        task_id="get_data",
        python_callable=get_data,
        requirements=["twelvedata", "pendulum", "lazy_object_proxy"],
        op_kwargs={"logical_date": "{{ logical_date }}"},
        serializer="cloudpickle",
    )

    save_data_op = PythonOperator(
        task_id="save_data",
        python_callable=save_data,
        op_kwargs={"data": get_data_op.output},
    )
