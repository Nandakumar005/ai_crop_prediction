import requests
import os
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_data(lat,lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(url).json()
    return{
        "temperature": response['main']['temp'],
        "humidity": response['main']['humidity'],
        "wind_speed": response['wind']['speed'],
        "weather_description": response['weather'][0]['description']
    }