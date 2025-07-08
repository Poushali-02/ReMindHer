import requests
from dotenv import load_dotenv
import os

load_dotenv()

# ==== Configure Gemini API ====
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not GOOGLE_PLACES_API_KEY:
    raise ValueError("GOOGLE_PLACES_API_KEY is not set in the environment variables.")

def get_doctors(location):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"gynecologist near {location}",
        "key": GOOGLE_PLACES_API_KEY
    }
    response = requests.get(endpoint, params=params)
    results = response.json().get("results", [])
    
    print('sent request to Google Places API with params:', params)
    
    doctors = []
    for r in results[:5]:  # Top 5 results
        doctors.append({
            "name": r.get("name"),
            "address": r.get("formatted_address"),
            "rating": r.get("rating", "N/A"),
            "maps_url": f"https://www.google.com/maps/place/?q=place_id:{r.get('place_id')}"
        })
    print(f'doctors = {response}\n{response.json()}')
    return doctors