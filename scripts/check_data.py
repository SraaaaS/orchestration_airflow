import duckdb
import pandas as pd
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")

def check_data():
    con = duckdb.connect(DB_PATH)

    result = con.execute("""
        SELECT *
        FROM weather
        ORDER BY date DESC
    """).fetchall()
    
    print(result)

    result = con.execute("""
    SELECT COUNT(*)
    FROM weather
    """).fetchone()

    print(f"Rows in weather table: {result[0]}")

    print(result)

    con.close()