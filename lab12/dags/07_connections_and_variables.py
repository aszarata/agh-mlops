import os
import json
from datetime import datetime, timedelta
from airflow import DAG

from airflow.providers.standard.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import Variable

save_query = """
INSERT INTO exchange_rates (symbol, rate) VALUES (%s, %s)
"""

def get_data(logical_date, api_key) -> dict:
    import os
    from twelvedata import TDClient

    td = TDClient(apikey=api_key)
    ts = td.exchange_rate(symbol="USD/EUR", date=logical_date.isoformat())
    return ts.as_json() 

def save_data(data: dict) -> None:
    POSTGRES_HOOK = "postgres_storage"
    postgres_hook = PostgresHook.get_hook(POSTGRES_HOOK)
    if not data:
        raise ValueError("No data received")
    
    parameters = {
        "symbol": data["symbol"],
        "rate": data["rate"]
    }

    postgres_hook.run(save_query, parameters)
    


with DAG(
    dag_id="connections_and_variables",
    start_date=datetime(2026, 1, 1),
) as dag:

    get_data_op = PythonVirtualenvOperator(
        task_id="get_data",
        python_callable=get_data,
        requirements=["twelvedata", "pendulum", "lazy_object_proxy"],
        op_kwargs={"logical_date": "{{ logical_date }}", "api_key": Variable.get("TWELVEDATA_API_KEY")},
        serializer="cloudpickle",
    )

    save_data_op = PythonOperator(
        task_id="save_data",
        python_callable=save_data,
        op_kwargs={"data": get_data_op.output},
    )
