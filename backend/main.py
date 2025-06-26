from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import json

from utils.nasa_power_loader import fetch_nasa_power_data
from extractor import get_data_disasters
from utils.gdacs_data_loader import fetch_gdacs_events
from utils.emdat import parse_emdat_excel_local

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("API_KEY"),  # убедись, что в .env ключ называется API_KEY
    base_url="https://openrouter.ai/api/v1"
)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(msg: ChatMessage):
    gdacs_data = fetch_gdacs_events()
    
    if not gdacs_data:
        summary = "Данные из GDACS недоступны."
    else:
        summary = "\n".join([
            f"{e['event_type']} в {e.get('country', 'неизвестно')} ({e['date']}), "
            f"магнитуда: {e.get('magnitude', '?')}, цвет: {e.get('color', '?')}"
            for e in gdacs_data[:5]
        ])

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a climate disaster intelligence assistant with access to global disaster data "
                    "(e.g., GDACS alerts, NASA POWER climate indicators, NOAA historical trends).\n\n"
                    "Your role is to:\n"
                    "1. Clearly mention natural disasters happening around the region that mentioned.\n"
                    "Be accurate and clearly separate:\n"
                    "- Confirmed events\n"
                    "- Forecasts\n"
                    "- Uncertainty\n\n"
                    "Make Your answer in 1-2 sentences for regular user"
                )
            },
            {
                "role": "user",
                "content": f"{msg.message}\n\nВот данные из GDACS:\n{summary}"
            }
        ]
    )

    reply = response.choices[0].message.content
    return {"reply": reply}



@app.get("/disasters")
def read_disasters():
    return get_data_disasters()

@app.get("/gdacs")
def gdacs_api():
    return fetch_gdacs_events()

@app.get("/emdat")
def emdat_data():
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir,'utils', 'LSTM', 'data', 'events.json')

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return JSONResponse(content=data)

@app.get("/country_desc")
def emdat_data():
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir,'utils', 'LSTM', 'data', 'countries.json')

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return JSONResponse(content=data)



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
