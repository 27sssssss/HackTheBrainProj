from app.utils.extractor import get_data_disasters
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.gdacs_data_loader import fetch_gdacs_events

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
def read_disasters():
    return fetch_gdacs_events()