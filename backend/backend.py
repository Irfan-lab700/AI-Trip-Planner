from backend.weather import getweather
from backend.searchhotel import search_hotels, get_destid
from backend.searchflight import get_flights
from backend.llm_service import generate_itinerary
from concurrent.futures import ThreadPoolExecutor, as_completed
def generate_trip_plan(trip_data):
    source = trip_data["source"]
    destination = trip_data["destination"]
    days = trip_data["days"]
    budget = trip_data["budget"]
    travellers = trip_data["num_travellers"]
    travel_date = trip_data["travel_date"]

    dest_id = get_destid(destination)
    results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            "source_weather": executor.submit(getweather, source, travel_date, days),
            "destination_weather": executor.submit(getweather, destination, travel_date, days),
            "hotels": executor.submit(search_hotels, dest_id, travel_date, days),
            "flights": executor.submit(get_flights, source, destination, travel_date),
        }

        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = f"Error: {str(e)}"

    weather = f"{results['source_weather']}\n\n{results['destination_weather']}"

    hotels = results["hotels"]
    flight = results["flights"]

    ai_plan = generate_itinerary(trip_data, weather, hotels, flight)

    return ai_plan