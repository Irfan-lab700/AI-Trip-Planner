import requests
import os
import json
import streamlit as st
from dotenv import load_dotenv
from backend.formatflight import format_skyscanner_response
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

@st.cache_data(ttl=86400, show_spinner=False)
def get_nearby_airport(city):
    url = "https://aerodatabox.p.rapidapi.com/airports/search/term"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }
    params = {"q": city, "limit": 5}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code != 200:
            return None
        data = response.json()
        for airport in data.get("items", []):
            if airport.get("iata"):
                return airport["iata"]
        return None
    except Exception as e:
        print(f"Error fetching airport for {city}: {e}")
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def search_flights_multi_leg(source_iata, dest_iata, date, return_date=None):
    url = "https://skyscanner-flights-travel-api.p.rapidapi.com/flights/searchFlightsMultiStops"
    legs = [{"originSkyId": source_iata, "destinationSkyId": dest_iata, "date": date}]
    if return_date:
        legs.append({"originSkyId": dest_iata, "destinationSkyId": source_iata, "date": return_date})
    querystring = {
        "adults": "1",
        "cabinClass": "economy",
        "currency": "INR",
        "legs": json.dumps(legs)
    }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "skyscanner-flights-travel-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        return format_skyscanner_response(response.json())
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_flights(source, destination, travel_date):
    source_iata = get_nearby_airport(source)        
    dest_iata = get_nearby_airport(destination)     

    if not source_iata or not dest_iata:
        return "❌ Airport not found"

    return search_flights_multi_leg(source_iata, dest_iata, travel_date)