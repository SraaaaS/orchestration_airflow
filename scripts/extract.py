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



# from datetime import datetime
# import pandas as pd
# import requests
# import duckdb
# import os


# DB_PATH = "/opt/airflow/weather.db"


# def extract(**context):

#     # -----------------------------
#     # Connexion à DuckDB
#     # -----------------------------
#     con = duckdb.connect(DB_PATH)

#     # -----------------------------
#     # Vérifie si la table existe déjà
#     # -----------------------------
#     table_exists = con.execute("""
#         SELECT COUNT(*)
#         FROM information_schema.tables
#         WHERE table_name = 'weather'
#     """).fetchone()[0]

#     # -----------------------------
#     # CAS 1 : premier lancement
#     # -> récupération historique complète
#     # -----------------------------
#     if table_exists == 0:

#         start_date = "2024-01-01"

#     # -----------------------------
#     # CAS 2 : pipeline déjà alimentée
#     # -> récupération incrémentale
#     # -----------------------------
#     else:

#         last_date = con.execute("""
#             SELECT MAX(date)
#             FROM weather
#         """).fetchone()[0]

#         start_date = last_date.strftime("%Y-%m-%d")

#     # -----------------------------
#     # Date actuelle
#     # -----------------------------
#     end_date = datetime.now().strftime("%Y-%m-%d")

#     print(f"Start date: {start_date}")
#     print(f"End date: {end_date}")

#     # -----------------------------
#     # API Open-Meteo
#     # -----------------------------
#     url = (
#         "https://archive-api.open-meteo.com/v1/archive"
#         "?latitude=45.75"
#         "&longitude=4.85"
#         f"&start_date={start_date}"
#         f"&end_date={end_date}"
#         "&daily=temperature_2m_mean"
#         "&timezone=Europe%2FParis"
#     )

#     response = requests.get(url)

#     data = response.json()

#     # -----------------------------
#     # DataFrame
#     # -----------------------------
#     df = pd.DataFrame({
#         "date": data["daily"]["time"],
#         "T_journaliere": data["daily"]["temperature_2m_mean"]
#     })

#     print(df.head())
#     print(df.tail())
#     print(f"Nombre de lignes récupérées : {len(df)}")

#     # -----------------------------
#     # Sauvegarde CSV
#     # -----------------------------
#     os.makedirs("/opt/airflow/data", exist_ok=True)

#     df.to_csv(
#         "/opt/airflow/data/raw_weather_data.csv",
#         index=False
#     )

#     con.close()