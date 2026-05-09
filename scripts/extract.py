import requests
import pandas as pd
import os 
os.makedirs("/opt/airflow/data", exist_ok=True)

def extract(**context):
    start_date = context["prev_ds"]
    end_date = context["ds"]

    base_url = "https://archive-api.open-meteo.com/v1/archive?"
    params = {"latitude":45.7485,
              "longitude":4.8467, 
              "start_date": start_date,
              "end_date": end_date,
              "hourly": "temperature_2m"
              }
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"API  error/ {response.status_code} - {response.text}")
    
    data = response.json()

    if "hourly" not in data:
        raise Exception("Missing 'hourly in API response")

    df = pd.DataFrame({"time" : data["hourly"]["time"], 
                       "temperature_2m" : data["hourly"]["temperature_2m"]
                       })
    df.to_csv("/opt/airflow/data/raw_weather_data.csv", index=False)
    #df.to_csv("data/raw_weather_data.csv", index=False)
    return df



