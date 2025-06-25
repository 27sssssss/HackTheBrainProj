from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from utils.nasa_power_loader import fetch_nasa_power_data
from extractor import get_data_disasters
from utils.gdacs_data_loader import fetch_gdacs_events

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/disasters")
def read_disasters():
    return get_data_disasters()

@app.get("/gdacs")
def gdacs_api():
    return fetch_gdacs_events()

@app.get("/nasa")
def nasa_api():
    data = fetch_gdacs_events()
    all_weather = []
    for item in data:
        lat = item["lat"]
        lon = item["lng"]
        date = datetime.fromisoformat(item['date']).strftime("%Y%m%d")
        disaster_info = {
            "event_type": item["event_type"],
            "disaster_date": item["date"],
            "color": item["color"],
            "severity": item["severity"],
            "magnitude": item["magnitude"]
        }

        try:
            weather_data = fetch_nasa_power_data(
                lat=lat,
                lon=lon,
                start_date=date,
                end_date=date,
            )

            for day in weather_data:
                day.update(disaster_info)
                all_weather.append(day)

        except Exception as e:
            print(f"⚠️ Ошибка для координат ({lat}, {lon}): {e}")

    return all_weather