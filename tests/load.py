import pandas as pd
import duckdb

def load():
    df = pd.read_csv("data/daily_weather_data.csv") 
    #df["date"] = pd.to_datetime(df["date"]).dt.date    

    con = duckdb.connect("weather.db") #beware

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
    
if __name__ == "__main__":
    load()