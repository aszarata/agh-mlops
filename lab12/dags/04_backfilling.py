import pandas as pd
import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task

@task
def get_data() -> dict:
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=40.7128&longitude=-74.006&start_date=2025-01-01&end_date=2025-01-31&daily=temperature_2m_max,temperature_2m_min&timezone=America/New_York"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["daily"]

@task
def transform(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    return df

@task
def save_data(df: pd.DataFrame) -> None:
    df.to_csv("weather_ny_jan_2025.csv", index=False)

with DAG(
    dag_id="backfilling",
    start_date=datetime(2026, 1, 1),
    schedule=timedelta(days=7),
) as dag:
    
    raw_data = get_data()
    transformed_data = transform(raw_data)
    save_data(transformed_data)