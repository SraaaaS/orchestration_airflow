from datetime import datetime
import pandas as pd
import requests
import psycopg2
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")


def extract():

    print("Connexion à la base de données weather_db")
    con = psycopg2.connect(
    host="postgres",
    database="weather_db",
    user="airflow",
    password="airflow"
)
    cursor = con.cursor()

    cursor.execute("""
            SELECT EXISTS(
                   SELECT 1
                   FROM information_schema.tables
                   WHERE table_name = 'weather'
                   )
                   """)

    table_exists = cursor.fetchone()[0]

    if not table_exists :
        start_date = "2024-01-01"
    else:
        cursor.execute("""
                       SELECT MAX(time)
                       FROM weather
                       """)
        last_date = cursor.fetchone()[0]
        start_date = last_date.strftime("%Y-%m-%d")
    

#     try:
    #     cursor.execute("""
    #         SELECT MAX(time)
    #         FROM weather
    #     """)

    #     last_date = cursor.fetchone()[0]

    #     if last_date is None:
    #         start_date = "2024-01-01"
    #     else:
    #         start_date = last_date.strftime("%Y-%m-%d")

#      except psycopg2.errors.UndefinedTable:
    #     con.rollback()
    #     start_date = "2024-01-01"


    end_date = datetime.now().strftime("%Y-%m-%d")


    # print("Verification de l'existence de la table")
    # table_exists = con.execute("""
    #     SELECT COUNT(*)
    #     FROM information_schema.tables
    #     WHERE table_name = 'weather'
    # """).fetchone()[0]

    # if table_exists == 0:
    #     start_date = "2024-01-01"

    # else:
    #     last_date = con.execute("""
    #         SELECT MAX(time)
    #         FROM weather
    #     """).fetchone()[0]        
    #     start_date = str(last_date)[:10]
        
    # end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Extraction du {start_date} au {end_date}")

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


    print(df)
    
    print(f"Sauvegarde de {len(df)} lignes sous le format .csv")
    os.makedirs("/opt/airflow/data", exist_ok=True)

    df.to_csv(CSV_PATH, index=False)

    print(f"Fichier sauvegardé sous {CSV_PATH}")
    cursor.close()
    con.close()