import os
import json
import requests
from dotenv import load_dotenv


def get_gemini_summary(weather, location, crops, soil_npk, farm_info):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    params = {"key": api_key}

    crop_lines = ", ".join(crops)

    prompt = f"""
You are an agriculture advisor for Indian farmers.

Location: {location.get('district')}, {location.get('state')}.
Weather: temperature {weather.get('temperature')} C, humidity {weather.get('humidity')}%, rainfall {weather.get('rainfall') or 0} mm.

Soil Nutrients: Nitrogen={soil_npk.get('N')}, Phosphorus={soil_npk.get('P')}, Potassium={soil_npk.get('K')}, pH={soil_npk.get('ph')}.
Farm Size: {farm_info.get('farm_size', 'Not specified')} acres.
Soil Type: {farm_info.get('soil_type', 'Not specified')}.
Terrain: {farm_info.get('terrain', 'Not specified')}.

Top predicted crops: {crop_lines}.

Based on all the above data, recommend the single best crop from the list for this farmer. Explain why it is the best choice considering the soil nutrients, weather, terrain, farm size and market conditions. Keep the advice under 150 words and farmer-friendly.

Return only valid JSON:
{{
  "best_crop": "crop name",
  "summary": "your advice here"
}}
""".strip()

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"},
    }

    try:
        response = requests.post(url, params=params, json=payload, timeout=30)
        data = response.json()
        if "candidates" in data:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
    except Exception as e:
        print("Gemini API error:", e)

    return {"best_crop": "", "summary": "Gemini is currently unavailable. Please try again later."}
