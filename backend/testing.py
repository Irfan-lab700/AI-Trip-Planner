from flight import get_nearby_airports, get_flights

source_city = "Delhi"
destination_city = "Mumbai"
travel_date = "2026-07-15"

source_airports = get_nearby_airports(source_city)
destination_airports = get_nearby_airports(destination_city)

print("Source:", source_airports)
print("Destination:", destination_airports)

all_flights = []

for s_airport in source_airports:
    for d_airport in destination_airports:
        flights = get_flights(s_airport, d_airport, travel_date)
        all_flights.extend(flights)

print("Flights:", all_flights[:3])
