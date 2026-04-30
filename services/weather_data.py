import os
from pathlib import Path
import requests
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise RuntimeError("WEATHER_API_KEY is not set in .env")


def get_weather_data(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception(
            f"Error fetching weather data ({response.status_code}): {data.get('message', 'Unknown error')}"
        )

    main = data.get("main", {})
    rain = data.get("rain", {})

    return {
        "temperature": main.get("temp"),
        "humidity": main.get("humidity"),
        "rainfall": rain.get("1h"),
    }