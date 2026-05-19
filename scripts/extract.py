from datetime import datetime, timedelta
import pandas as pd
import requests
import duckdb
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")


def extract():

    print("Connexion à la base de données weather.db")
    con = duckdb.connect(DB_PATH)

    print("Verification de l'existence de la table")
    table_exists = con.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'weather'
    """).fetchone()[0]

    if table_exists == 0:
        start_date = "2024-01-01"

    else:
        last_date = con.execute("""
            SELECT MAX(date)
            FROM weather
        """).fetchone()[0]        
        start_date = last_date
        
    end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"start_date = {start_date}")
    print(f"end_date = {end_date}")


    print("Récuperation des données via l'API météo")
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
    
    df = pd.DataFrame({"time" : data["hourly"]["time"], 
                       "temperature_2m" : data["hourly"]["temperature_2m"]
                       })
    
    df["time"] = pd.to_datetime(df["time"], utc=True)

    now = pd.Timestamp.now(tz="UTC")

    df = df[df["time"] <= now]

    # now = pd.Timestamp.utcnow()
    # df = df[df["time"]<= now]

    # if os.path.exists(CSV_PATH):
    #     old_df = pd.read_csv(CSV_PATH)
    #     old_df["time"] = pd.to_datetime(old_df["time"])

    #     df = pd.concat([old_df, df])
    #     df = df.drop_duplicates(subset=["time"])
    

    print(df)
    
    print("Sauvegarde sous le format .csv")
    os.makedirs("/opt/airflow/data", exist_ok=True)

    df.to_csv(CSV_PATH, index=False)

    print("Fichier sauvegardé sous /opt/airflow/data/raw_weather_data.csv")
    con.close()