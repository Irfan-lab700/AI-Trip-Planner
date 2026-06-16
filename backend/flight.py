import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AVIATION_API_KEY")

def get_nearby_airports(city):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": API_KEY,
        "search": city
    }
    response = requests.get(url, params = params)
    data = response.json()
    print(data['data'][0])
    iata_codes = []
    for airport in data['data']:
        if airport.get('iata_code'):
            iata_codes.append(airport['iata_code'])
    return iata_codes[:3]  
def get_flights(source_iata, dest_iata, travel_date):
    url = "http://api.aviationstack.com/v1/flights"
    
    params = {
        "access_key": API_KEY,
        "dep_iata": source_iata,
        "arr_iata": dest_iata,
        "flight_date": travel_date
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    flights_list = []
    
    for flight in data['data']:
        flight_info = {
            "airline": flight.get("airline", {}).get("name"),
            "flight_number": flight.get("flight", {}).get("iata"),
            "departure_airport": flight.get("departure", {}).get("airport"),
            "arrival_airport": flight.get("arrival", {}).get("airport"),
            "departure_time": flight.get("departure", {}).get("scheduled"),
            "arrival_time": flight.get("arrival", {}).get("scheduled"),
            "status": flight.get("flight_status")
        }
        
        flights_list.append(flight_info)
    
    return flights_list

        