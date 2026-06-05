import os
from urllib import response
import requests
import streamlit as st
from datetime import datetime, timedelta
from backend.formathotel import format_hotels
from dotenv import load_dotenv
load_dotenv()
@st.cache_data(ttl=86400 ,show_spinner=False)
def search_hotels(city,travel_date,days):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {
        "dest_id":city,
        "search_type": "CITY",
        "arrival_date": travel_date,
        "departure_date": str((datetime.strptime(travel_date, "%Y-%m-%d") + timedelta(days=days)).date()),
        "adults": "1",
        "room_qty": "1",
        "page_number": "1",
        "units": "metric",
        "temperature_unit": "c",
        "languagecode": "en-us",
        "currency_code": "INR"
    }
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=10)
    data = response.json()
    return format_hotels(data)
@st.cache_data(ttl=3600)
def get_destid(city):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    querystring = {"query":city}
    headers = {
	"x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
	"x-rapidapi-host": "booking-com15.p.rapidapi.com",
	"Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=5)
    data = response.json()
    # SAFE CHECK
    if "data" not in data or not data["data"]:
        return None

    for item in data["data"]:
        if item.get("dest_type") == "city":
            return item.get("dest_id")

    return data["data"][0].get("dest_id")