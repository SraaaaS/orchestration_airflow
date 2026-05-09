import pandas as pd
import duckdb
# import os
# from dotenv import load_dotenv

# load_dotenv()
# DB_PATH = os.getenv("WEATHER_DB_PATH")

def load():
    df = pd.read_csv("/opt/airflow/data/daily_weather_data.csv") 
    #df["date"] = pd.to_datetime(df["date"]).dt.date    
    #df = df[["time","T_moyenne"]]

    con = duckdb.connect("/opt/airflow/data/weather.db") 

    con.execute("""CREATE TABLE IF NOT EXISTS weather (
                date DATE,
                T_journaliere DECIMAL(5,2)
                )
                """)
    
    
    con.register("temp_df", df)
    
    con.execute("""INSERT INTO weather
                    SELECT *
                    FROM temp_df
                    WHERE CAST(date AS DATE) NOT IN (SELECT date FROM weather)
                """)
    
    result = con.execute("SELECT COUNT(*) FROM weather ").fetchone()
    print(f"Rows in weather table: {result[0]}")

    test = con.execute("""SELECT * FROM weather 
                       """).fetchall()
    #
                       # ORDER BY date DESC 
                       #LIMIT 10
    print(test)
