import duckdb
import pandas as pd
# import os
# from dotenv import load_dotenv

# load_dotenv()
# DB_PATH = os.getenv("WEATHER_DB_PATH")

def check_data():
    con = duckdb.connect("/opt/airflow/data/weather.db")

    result = con.execute("""
        SELECT *
        FROM weather
        ORDER BY date DESC
    """).fetchall()

    print(result)
