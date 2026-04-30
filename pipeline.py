from services.weather_data import get_weather_data
from services.location_service import get_location_details
from services.crop_service import predict_top_crops
from services.market_service import get_best_price

VALID_CROPS = ["rice", "wheat", "maize", "cotton", "tomato"]


def full_pipeline(lat, lon, N, P, K, ph=6.5):
    weather = get_weather_data(lat, lon)
    temp = weather["temperature"]
    humidity = weather["humidity"]
    rainfall = weather["rainfall"] or 100

    location = get_location_details(lat, lon)
    state = location["state"]
    district = location["district"]

    crops = predict_top_crops(N, P, K, temp, humidity, ph, rainfall)
    crops = [c for c in crops if c in VALID_CROPS]

    ranked = []
    for crop in crops:
        price = get_best_price(crop, state, district)
        ranked.append((crop, price))

    ranked.sort(key=lambda x: x[1], reverse=True)

    return {
        "weather": weather,
        "location": {"state": state, "district": district},
        "crops": ranked,
    }
