import os
import random
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

BASE_PRICES = {
    "rice": 2500, "maize": 2000, "jute": 4000, "cotton": 6000,
    "coconut": 3000, "papaya": 2000, "orange": 4000, "apple": 8000,
    "muskmelon": 2000, "watermelon": 1500, "grapes": 6000, "mango": 4000,
    "banana": 1500, "pomegranate": 8000, "lentil": 6000, "blackgram": 7000,
    "mungbean": 7500, "mothbeans": 6000, "pigeonpeas": 7000,
    "kidneybeans": 8000, "chickpea": 5500, "coffee": 15000,
}

CROP_MAPPING = {
    "rice": ["paddy", "rice"],
    "maize": ["maize"],
    "pigeonpeas": ["arhar", "tur"],
    "blackgram": ["urad"],
    "mungbean": ["moong"],
    "lentil": ["masur"],
    "chickpea": ["gram", "chana"],
    "cotton": ["cotton"],
    "banana": ["banana"],
    "mango": ["mango"],
    "grapes": ["grapes"],
}

API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

def get_live_market_data(crops, state=None, days=7):
    load_dotenv()
    api_key = os.getenv("MARKET_API_KEY")

    market_data = {}
    result = []

    if api_key:
        try:
            params = {
                "api-key": api_key,
                "format": "json",
                "limit": 1000
            }

            response = requests.get(API_URL, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json().get("records", [])

                cutoff_date = datetime.now() - timedelta(days=days)

                for record in data:
                    comm = record.get("commodity", "").lower()
                    rec_state = record.get("state", "")
                    date_str = record.get("arrival_date", "")

                    if state and state.lower() not in rec_state.lower():
                        continue

                    try:
                        rec_date = datetime.strptime(date_str, "%d/%m/%Y")
                        if rec_date < cutoff_date:
                            continue
                    except:
                        continue

                    try:
                        price = float(record.get("modal_price", 0))
                        if price <= 0:
                            continue
                    except:
                        continue

                    if comm not in market_data:
                        market_data[comm] = []

                    market_data[comm].append(price)

        except Exception as e:
            print("Market API error:", e)

    for crop in crops:
        crop_lower = crop.lower()
        keywords = CROP_MAPPING.get(crop_lower, [crop_lower])

        matched_prices = []
        matched_commodities = []

        for comm, prices in market_data.items():
            if any(keyword in comm for keyword in keywords):
                matched_prices.extend(prices)
                matched_commodities.append(comm)

        if matched_prices:
            avg_price = sum(matched_prices) / len(matched_prices)

            confidence = "high" if len(matched_prices) > 5 else "medium"

            result.append({
                "crop": crop,
                "estimated_value": round(avg_price),
                "unit": "Rs/quintal",
                "confidence": confidence,
                "data_points": len(matched_prices),
                "source": "live_market_api",
                "matched_commodities": list(set(matched_commodities))
            })

        else:
            base_price = BASE_PRICES.get(crop_lower, 3000)
            simulated = base_price * (1 + random.uniform(-0.05, 0.05))

            result.append({
                "crop": crop,
                "estimated_value": round(simulated),
                "unit": "Rs/quintal",
                "confidence": "low",
                "data_points": 0,
                "source": "fallback_estimation",
                "matched_commodities": []
            })

    result.sort(key=lambda x: x["estimated_value"], reverse=True)

    return result