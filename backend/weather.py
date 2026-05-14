from datetime import datetime, timedelta
import requests
from backend.formatweather import format_weather
def getweather(city,date,days):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url, timeout=5)
    data = response.json()
    if "results" in data:
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
    else:
        return ("location not found")
    start_date_obj = datetime.strptime(date, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=days-1)
    end_date = end_date_obj.strftime("%Y-%m-%d")

    weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lat}&longitude={lon}"
    f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
    f"&start_date={date}"
    f"&end_date={end_date}"
    f"&timezone=auto"
)
    
    response = requests.get(weather_url, timeout=10)
    data = response.json()
    return format_weather(data, city)
