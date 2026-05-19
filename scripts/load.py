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
            date DATE,
            T_journaliere DECIMAL(5,2)
        )
    """)

    con.register("temp_df", df)

    print("Ajout des nouvelles valeurs dans la table")
    con.execute("""
        INSERT INTO weather
        SELECT *
        FROM temp_df
        WHERE CAST(date AS DATE)
        NOT IN (
            SELECT date FROM weather
        )
    """)

    con.close()