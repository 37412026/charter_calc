from fastapi import FastAPI
import json

app = FastAPI(title="Aviation & Vehicle API")

# Health check endpoint
@app.get("/")
def home():
    return {"status": "API running successfully"}

# Airport lookup endpoint
@app.get("/airport")
def get_airport(iata: str):
    try:
        with open("data/airports.json", "r") as f:
            airports = json.load(f)
    except FileNotFoundError:
        return {"error": "airports.json not found"}
    
    for airport in airports:
        if airport["iata"].upper() == iata.upper():
            return airport
    
    return {"error": "Airport not found"}
