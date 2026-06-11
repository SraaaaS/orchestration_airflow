import duckdb
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
def check_data():
    print("Connexion à la base de données")
    con = duckdb.connect(DB_PATH)

    # -------------------------------------------------------------
    # 1. VÉRIFICATION DE LA TABLE BRUTE (INGESTION OUK)
    # -------------------------------------------------------------
    print("--- [1/2] DERNIÈRES DONNÉES HORAIRES BRUTES (WEATHER) ---")
    raw_data = con.execute("""
        SELECT *
        FROM weather
        ORDER BY time DESC
        LIMIT 5
    """).fetchall()
    print(raw_data)
    
    raw_count = con.execute("SELECT COUNT(*) FROM weather").fetchone()[0]
    print(f"Nombre total de lignes brutes : {raw_count}\n")

    # -------------------------------------------------------------
    # 2. VÉRIFICATION DE LA TABLE FINALE dbt (TRANSFORMATION OK)
    # -------------------------------------------------------------
    print("--- [2/2] DERNIÈRES MOYENNES JOURNALIÈRES (DBT MART) ---")
    # Note : remplace 'daily_temperature' par 'daily_temperatures' (avec un s) 
    # si c'est le nom exact de ton fichier SQL dbt.
    dbt_data = con.execute("""
        SELECT *
        FROM daily_temperature
        ORDER BY date DESC
        LIMIT 5
    """).fetchall()
    print(dbt_data)
    
    dbt_count = con.execute("SELECT COUNT(*) FROM daily_temperature").fetchone()[0]
    print(f"Nombre total de jours calculés : {dbt_count}")

    con.close()