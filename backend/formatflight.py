def format_skyscanner_response(data):
    try:
        itineraries = data.get("itineraries", [])

        if not itineraries:
            return {"status": "empty", "flights": []}

        flights = []

        for itin in itineraries[:5]:
            legs = itin.get("legs", [])

            journey = []

            for leg in legs:
                journey.append({
                    "from": leg.get("origin", {}).get("displayCode"),
                    "to": leg.get("destination", {}).get("displayCode"),
                    "departure": leg.get("departure"),
                    "arrival": leg.get("arrival"),
                    "duration": leg.get("durationInMinutes"),
                    "airline": leg.get("carriers", {}).get("marketing", [{}])[0].get("name")
                })

            flights.append({
                "price": itin.get("price", {}).get("formatted"),
                "legs": journey
            })

        return {"status": "success", "flights": flights}

    except Exception as e:
        return {"status": "error", "message": str(e)}