import pandas as pd
import os
from dotenv import load_dotenv 
load_dotenv()

DB_PATH = os.getenv("WEATHER_DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")

os.makedirs("/opt/airflow/data", exist_ok=True)

def transform():
    df = pd.read_csv(CSV_PATH) 
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date

    print("Calcul de la moyenne des temperatures par jour")
    daily_df = df.groupby("date")["temperature_2m"].mean().reset_index()

    print("Renommage de la colonne des temperature")
    daily_df.rename(columns={"temperature_2m":"T_moyenne"}, inplace=True)

    print("Formatage à deux decimales près de la valeur de la temperature moyenne")
    daily_df["T_moyenne"] = daily_df["T_moyenne"].apply(lambda x: '{:,.2f}'.format(x))

    print("ré-enregistrement de la transformation au format csv")
    daily_df.to_csv(CSV_PATH, index=False)
    return daily_df


if __name__ == "__main__":
    df = transform()
    print(df)