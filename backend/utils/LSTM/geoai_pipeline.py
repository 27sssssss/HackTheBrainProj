import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from gee_climate import init_gee, get_climate_features
from gdacs_data_loader import fetch_gdacs_events
from nasa_power_loader import fetch_nasa_power_data
from google_engine import fetch_gee_data
from model import update_model, predict_risk

LAT, LON = 35.0, 139.0
TIME_WINDOW = 14


def label_climate_with_disasters(climate_df, disaster_df, lat, lon):
    disaster_df['date'] = pd.to_datetime(disasters_df['date'])
    labeled = []
    for _, row in climate_df.iterrows():
        date = row['date']
        nearby_disasters = disaster_df[
            (abs(disaster_df['lat'] - lat) <= 1) &
            (abs(disaster_df['lng'] - lon) <= 1) &
            (abs((disaster_df['date'] - date).dt.days) <= 2)
        ]
        label = 1 if not nearby_disasters.empty else 0
        labeled.append(label)
    climate_df['label'] = labeled
    return climate_df.dropna()


def build_sequences(df, time_window):
    features = ['temperature', 'precipitation', 'humidity', 'ndvi', 'lst']
    df = df.dropna(subset=features + ['label']).reset_index(drop=True)
    X, y = [], []
    for i in range(len(df) - time_window):
        X.append(df[features].iloc[i:i+time_window].values)
        y.append(df['label'].iloc[i + time_window])
    return np.array(X), np.array(y)


def collect_and_train(start_date, end_date, lat=LAT, lon=LON):
    print(f"Data collect {start_date} по {end_date}...")
    init_gee()
    nasa_df = fetch_nasa_power_data(lat, lon, start_date.replace("-", ""), end_date.replace("-", ""))
    gee_df = fetch_gee_data(lat, lon, start_date, end_date)
    disasters_df = fetch_gdacs_events(limit_days=365)

    df = pd.merge(nasa_df, gee_df, on="date", how="outer")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values("date")
    df = label_climate_with_disasters(df, disasters_df, lat, lon)

    X, y = build_sequences(df, TIME_WINDOW)
    np.save("data/X.npy", X)
    np.save("data/y.npy", y)
    df.to_csv("data/labeled_data.csv", index=False)

    print("Learning...")
    update_model(X, y)
    return df


def run_pipeline():
    collect_and_train("2024-01-01", "2024-06-30")
    collect_and_train("2025-06-01", "2024-06-30")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    init_gee()
    nasa_today = fetch_nasa_power_data(LAT, LON, today.replace("-", ""), today.replace("-", ""))
    gee_today = fetch_gee_data(LAT, LON, today, today)

    df_today = pd.merge(nasa_today, gee_today, on="date", how="outer")
    df_today = df_today.dropna()

    if len(df_today) >= TIME_WINDOW:
        X_today = df_today[['temperature', 'precipitation', 'humidity', 'ndvi', 'lst']].tail(TIME_WINDOW).values
        X_today = np.expand_dims(X_today, axis=0)
        risk = predict_risk(X_today)
        print(f"Risk is  = {risk:.2f}")
    else:
        print("Not engough data")


if __name__ == "__main__":
    run_pipeline()
