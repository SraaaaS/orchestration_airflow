import pandas as pd
import duckdb
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")

def load():

    df = pd.read_csv(CSV_PATH)
    con = duckdb.connect(DB_PATH)

    print("creation de la table en cas d'inexistence")
    con.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            time VARCHAR UNIQUE,
            temperature_2m DECIMAL(5,2)
        )
    """)

    con.register("temp_df", df)

    print("Insertion des données horaires brutes dans la table weather")
    con.execute("""
        INSERT INTO weather
        SELECT time, temperature_2m
        FROM temp_df
        ON CONFLICT (time)
        DO UPDATE
        SET temperature_2m = EXCLUDED.temperature_2m
    """)

    con.close()
    print("Chargement terminé avec succès")