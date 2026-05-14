def format_hotels(data):
    if "data" not in data or "hotels" not in data["data"]:
        return "No hotels found"

    hotels = []

    for h in data["data"]["hotels"][:10]:
        prop = h.get("property", {})

        price = (
            prop.get("priceBreakdown", {})
                .get("grossPrice", {})
                .get("value")
        )

        if price is None:
            continue

        hotel = {
            "name": prop.get("name", "Unknown"),
            "price": round(price),
            "rating": prop.get("reviewScore", 0),
            "location": prop.get("wishlistName", "Unknown")
        }

        hotels.append(hotel)

    hotels = sorted(hotels, key=lambda x: x["price"])

    return hotels[:5]