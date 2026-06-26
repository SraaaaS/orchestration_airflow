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
    
    print("--- [1/2] DERNIÈRES DONNÉES HORAIRES BRUTES (WEATHER) ---")
    cursor.execute("""
        SELECT *
        FROM weather
        ORDER BY time DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    con.commit()
    

    cursor.execute("""SELECT COUNT(*) FROM weather
                   """)
    result = cursor.fetchone()
    print(f"Nombre de lignes : {result[0]}")

    print("--- [2/2] DERNIÈRES MOYENNES JOURNALIÈRES (DBT MART) ---")
    cursor.execute("""
        SELECT *
        FROM daily_temperature
        ORDER BY date DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    con.commit()


    cursor.execute("""SELECT COUNT(*) FROM daily_temperature
                   """)
    result = cursor.fetchone()
    print(f"Nombre total de jours calculés : {result[0]}")

    con.commit()


    cursor.close()
    con.close()
