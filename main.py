from fastapi import FastAPI
import json
import os

app = FastAPI(title="Aviation & Vehicle API")

AIRPORTS = {}
DATA_FILE = os.path.join("data", "airports.json")

# Load airports safely at startup
try:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            AIRPORTS = json.load(f)
except Exception as e:
    AIRPORTS = {}
    print("ERROR loading airports:", e)

@app.get("/")
from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "airports.json")

# Load airports safely
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        AIRPORTS = json.load(f)
except Exception as e:
    AIRPORTS = {}
    print("Failed to load airports:", e)


@app.get("/")
def root():
    return {"status": "API running successfully"}


@app.get("/airport")
def get_airport(iata: str):
    if not iata:
        raise HTTPException(status_code=400, detail="IATA code is required")

    iata = iata.upper()

    for airport in AIRPORTS.values():
        if airport.get("iata", "").upper() == iata:
            return airport

    raise HTTPException(status_code=404, detail="Airport not found")

