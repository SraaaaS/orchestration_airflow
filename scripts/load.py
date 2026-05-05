import pandas as pd
import duckdb

def load():
    df = pd.read_csv("opt/airflow/data/daily_weather_data.csv")

    con = duckdb.connect("weather.db")

    con.register("temp_df", df)
    con.execute("DROP TABLE IF EXISTS weather")
    con.execute("""CREATE TABLE weather 
                AS SELECT * FROM temp_df""")
    
    result = con.execute("SELECT COUNT(*) FROM weather ").fetchone()
    print(f"Rows in weather table: {result[0]}")
    
if __name__ == "__main__":
    load()