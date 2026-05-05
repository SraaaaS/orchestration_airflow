import pandas as pd
import os

os.makedirs("opt/airflow/data", exist_ok=True)

def transform():
    df = pd.read_csv("opt/airflow/data/raw_weather_data.csv")
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date

    daily_df = df.groupby("date")["temperature_2m"].mean().reset_index()
    daily_df.rename(columns={"temperature_2m":"T_moyenne"}, inplace=True)
    daily_df["T_moyenne"] = daily_df["T_moyenne"].apply(lambda x: '{:,.2f}'.format(x))
    daily_df.to_csv("opt/airflow/data/daily_weather_data.csv")
    #daily_df.to_csv("data/daily_weather_data.csv", index=False)
    return daily_df


if __name__ == "__main__":
    df = transform()
    print(df)