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
def home():
    return {
        "status": "API running successfully",
        "airports_loaded": len(AIRPORTS)
    }

@app.get("/airport")
def get_airport(iata: str):
    try:
        if not AIRPORTS:
            return {"error": "Airport database not loaded"}

        for icao, airport in AIRPORTS.items():

            # HARD SAFETY CHECKS
            if not isinstance(airport, dict):
                continue

            airport_iata = airport.get("iata")

            if airport_iata and airport_iata.upper() == iata.upper():
                return {
                    "icao": icao,
                    "iata": airport_iata,
                    "name": airport.get("name"),
                    "city": airport.get("city"),
                    "state": airport.get("state"),
                    "country": airport.get("country"),
                    "lat": airport.get("lat"),
                    "lon": airport.get("lon")
                }

        return {"error": "Airport not found"}

    except Exception as e:
        # THIS PREVENTS INTERNAL SERVER ERROR
        return {
            "error": "Server error",
            "details": str(e)
        }
