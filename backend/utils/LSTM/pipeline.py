from nasa_power_loader import fetch_nasa_power_data
from google_engine import fetch_gee_data
from gdacs_data_loader import fetch_gdacs_events
from model import update_model, predict_risk
import pandas as pd
import numpy as np
from datetime import datetime

LAT, LON = 35.0, 139.0
START_DATE = "2024-01-01"
END_DATE = "2025-4-01"
TIME_WINDOW = 14

nasa_df = fetch_nasa_power_data(LAT, LON, START_DATE.replace("-", ""), END_DATE.replace("-", ""))
gee_df = fetch_gee_data(LAT, LON, START_DATE, END_DATE)
disasters_df = fetch_gdacs_events(limit_days=365)

df = pd.merge(nasa_df, gee_df, on="date", how="outer")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values("date")

disasters_df['date'] = pd.to_datetime(disasters_df['date'])
df['label'] = df['date'].apply(
    lambda d: int(
        any(abs((d - row['date']).days) <= 2 and
            abs(LAT - row['lat']) <= 1 and abs(LON - row['lng']) <= 1
            for _, row in disasters_df.iterrows())
    )
)

features = ['temperature', 'precipitation', 'humidity', 'ndvi', 'lst']
df = df.dropna(subset=features + ['label']).reset_index(drop=True)

X, y = [], []
for i in range(len(df) - TIME_WINDOW):
    X.append(df[features].iloc[i:i+TIME_WINDOW].values)
    y.append(df['label'].iloc[i + TIME_WINDOW])

X = np.array(X)
y = np.array(y)

np.save("data/X.npy", X)
np.save("data/y.npy", y)
update_model(X, y)

risk = predict_risk(X[-1:]) 