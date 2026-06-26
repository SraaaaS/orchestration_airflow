import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv 
load_dotenv()

#DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")

def load():

    df = pd.read_csv(CSV_PATH)
    con = psycopg2.connect(
        host="postgres",
        database="weather_db",
        user="airflow",
        password="airflow"
    )

    cursor = con.cursor()
    
    print("creation de la table en cas d'inexistence")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
        time TIMESTAMP PRIMARY KEY,
        temperature_2m DOUBLE PRECISION
        )
    """
    )
    

    rows = list(
        df[["time", "temperature_2m"]]
        .itertuples(index=False, name=None)
    )

    execute_values(
        cursor,
        """
        INSERT INTO weather(time, temperature_2m)
        VALUES %s
        ON CONFLICT (time)
        DO UPDATE SET
            temperature_2m = EXCLUDED.temperature_2m
        """,
        rows
    )

    # print("Insertion des données horaires brutes dans la table weather")
    # for _, row in df.iterrows():
    #     cursor.execute("""
    #                    INSERT INTO weather(time, temperature_2m)
    #                    VALUES (%s, %s)
    #                    ON CONFLICT(time)
    #                    DO UPDATE set
    #                    temperature_2m = EXCLUDED.temperature_2m
    #                    )
    #                 """,
    #                 (row["time"], row["temperature_2m"])
    #                 )
    con.commit()

    cursor.close()
    con.close()
    print("Chargement terminé avec succès")
                       

    # con.register("temp_df", df)
    # con.execute("""
    #     INSERT INTO weather
    #     SELECT time, temperature_2m
    #     FROM temp_df
    #     ON CONFLICT (time)
    #     DO UPDATE
    #     SET temperature_2m = EXCLUDED.temperature_2m
    # """)
