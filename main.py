from fastapi import FastAPI
import json
import os

app = FastAPI(title="Charter Calculator API")

# Load airports data
DATA_PATH = os.path.join("data", "airports.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    airports = json.load(f)

@app.get("/")
def home():
    return {"status": "API running successfully"}

@app.get("/airport")
def get_airport(iata: str):
    iata = iata.upper()
    if iata in airports:
        return airports[iata]
    return {"error": "Airport not found"}
