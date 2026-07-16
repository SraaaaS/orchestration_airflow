import psycopg2
import os
from dotenv import load_dotenv 
load_dotenv()


def check_data():
    print("Connexion à la base de données")
    con = psycopg2.connect(
        host="postgres",
        database="weather_db",
        user="airflow",
        password="airflow"
    )

    cursor = con.cursor()
    
    print("--- [1/2] DERNIÈRES DONNÉES HORAIRES BRUTES (STG_WEATHER) ---")
    cursor.execute("""
        SELECT *
        FROM stg_weather
        LIMIT 5
    """)

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    con.commit()
    

    cursor.execute("""SELECT COUNT(*) FROM weather
                   """)
    result = cursor.fetchone()
    print(f"Nombre d'heures recensées : {result[0]}")

    print("--- [2/2] DERNIÈRES MOYENNES JOURNALIÈRES (DBT MART) ---")
    cursor.execute("""
        SELECT *
        FROM daily_temperature
        LIMIT 5
    """)

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    con.commit()


    cursor.execute("""SELECT COUNT(*) FROM daily_temperature
                   """)
    result = cursor.fetchone()
    print(f"Nombre total de jours jusqu'à présent : {result[0]}")

    con.commit()


    cursor.close()
    con.close()
