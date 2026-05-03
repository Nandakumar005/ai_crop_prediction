import os
import random
import requests
from dotenv import load_dotenv

BASE_PRICES = {
    "rice": 2500, "maize": 2000, "jute": 4000, "cotton": 6000,
    "coconut": 3000, "papaya": 2000, "orange": 4000, "apple": 8000,
    "muskmelon": 2000, "watermelon": 1500, "grapes": 6000, "mango": 4000,
    "banana": 1500, "pomegranate": 8000, "lentil": 6000, "blackgram": 7000,
    "mungbean": 7500, "mothbeans": 6000, "pigeonpeas": 7000,
    "kidneybeans": 8000, "chickpea": 5500, "coffee": 15000,
}


def get_live_market_data(crops):
    load_dotenv()
    api_key = os.getenv("MARKET_API_KEY")

    result = []
    market_data = {}

    if api_key:
        try:
            url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={api_key}&format=json&limit=500"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for record in data.get("records", []):
                    comm = record.get("commodity", "").lower()
                    try:
                        price = float(record.get("modal_price", 0))
                    except (ValueError, TypeError):
                        price = 0
                    if comm and price > 0:
                        if comm not in market_data:
                            market_data[comm] = []
                        market_data[comm].append(price)
        except Exception as e:
            print("Market API error:", e)

    for crop in crops:
        crop_lower = crop.lower()
        live_price = None

        for comm, prices in market_data.items():
            if crop_lower in comm or comm in crop_lower:
                live_price = sum(prices) / len(prices)
                break

        if live_price is None:
            base_price = BASE_PRICES.get(crop_lower, 3000)
            live_price = base_price * (1 + random.uniform(-0.1, 0.1))

        result.append({
            "crop": crop,
            "estimated_value": round(live_price),
            "unit": "Rs/quintal"
        })

    result.sort(key=lambda x: x["estimated_value"], reverse=True)
    return result
