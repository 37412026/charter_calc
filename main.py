from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="Charter Airports API")

# Enable CORS so WordPress site can access the API
origins = ["*"]  # In production, replace * with your WordPress domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load airports JSON once at startup
try:
    with open("data/airports.json", "r", encoding="utf-8") as f:
        airports_data = json.load(f)
except FileNotFoundError:
    airports_data = {}
    print("airports.json not found!")

@app.get("/")
def home():
    return {"status": "API running successfully"}

# --- Search airports by letters (autocomplete) ---
@app.get("/airport")
def search_airports(search: str = Query(..., min_length=1), iata: str = None):
    results = []

    if iata:  # If IATA code is provided, return exact airport
        for airport in airports_data.values():
            if airport["iata"].upper() == iata.upper():
                return airport
        raise HTTPException(status_code=404, detail="Airport not found")

    # Otherwise, search by letters in IATA or city or name
    search_lower = search.lower()
    for airport in airports_data.values():
        if (airport["iata"].lower().startswith(search_lower) or
            airport["name"].lower().startswith(search_lower) or
            airport["city"].lower().startswith(search_lower)):
            results.append({
                "iata": airport["iata"],
                "name": airport["name"],
                "city": airport["city"]
            })
        if len(results) >= 10:  # Limit suggestions
            break

    return results
