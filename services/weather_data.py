import os

import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather_data(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()

        main = data.get("main", {})
        rain = data.get("rain", {})

        return {
            "temperature": main.get("temp"),
            "humidity": main.get("humidity"),
            "rainfall": rain.get("1h"),
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return {
            "temperature": None,
            "humidity": None,
            "rainfall": None,
        }
