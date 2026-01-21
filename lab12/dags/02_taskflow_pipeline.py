import pandas as pd
import requests
from airflow import DAG
from airflow.decorators import task



@task
def get_data() -> dict:
    print("Fetching data from API")

    url = "https://archive-api.open-meteo.com/v1/archive?latitude=40.7143&longitude=-74.006&start_date=2025-01-01&end_date=2025-12-31&hourly=temperature_2m&timezone=auto"

    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()
    data = {
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
    }
    return data


@task
def transform(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["temperature"] = df["temperature"].clip(lower=-20, upper=50)
    return df


@task 
def save_data(df: pd.DataFrame) -> None:
    print("Saving the data")
    df.to_csv("data.csv", index=False)


with DAG(dag_id="weather_data_classes_api"):
    data = get_data()
    transformed = transform(data)
    load = save_data(transformed)