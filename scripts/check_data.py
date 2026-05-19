import duckdb
import pandas as pd
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")

def check_data():
    print("Connexion à la base de données")
    con = duckdb.connect(DB_PATH)

    print("Affichage de toute la table en commencant par les nouvelles valeurs")
    result = con.execute("""
        SELECT *
        FROM weather
        ORDER BY date DESC
    """).fetchall()
    
    print(result)
    
    print("Nombre total de valeurs presentes dans la table")
    result = con.execute("""
    SELECT COUNT(*)
    FROM weather
    """).fetchone()

    print(f"Rows in weather table: {result[0]}")

    print(result)

    con.close()