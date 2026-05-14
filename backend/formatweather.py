def get_weather_description(code):
    weather_map = {
        # Clear / Clouds
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",

        # Fog
        45: "Fog 🌫️",
        48: "Depositing rime fog 🌫️",

        # Drizzle
        51: "Light drizzle 🌦️",
        53: "Moderate drizzle 🌦️",
        55: "Heavy drizzle 🌧️",

        # Freezing Drizzle
        56: "Light freezing drizzle 🧊🌦️",
        57: "Heavy freezing drizzle 🧊🌧️",

        # Rain
        61: "Light rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain 🌧️",

        # Freezing Rain
        66: "Light freezing rain 🧊🌧️",
        67: "Heavy freezing rain 🧊🌧️",

        # Snow
        71: "Light snow ❄️",
        73: "Moderate snow ❄️",
        75: "Heavy snow ❄️",

        # Snow grains
        77: "Snow grains 🌨️",

        # Rain showers
        80: "Light rain showers 🌦️",
        81: "Moderate rain showers 🌧️",
        82: "Heavy rain showers 🌧️",

        # Snow showers
        85: "Light snow showers ❄️",
        86: "Heavy snow showers ❄️",

        # Thunderstorm
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with hail ⛈️🧊",
        99: "Heavy thunderstorm with hail ⛈️🧊"
    }
    return weather_map.get(code, "Unknown")
def format_weather(data, city):
    if "daily" not in data:
        return f"Weather data not available for {city}"

    daily = data["daily"]
    result = f"Weather forecast for {city}:\n"

    for i in range(len(daily["time"])):
        date = daily["time"][i]
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        weather = get_weather_description(daily["weathercode"][i])

        result += (
            f"{date}: {weather}, "
            f"Temperature {temp_min}°C to {temp_max}°C\n"
        )

    return result