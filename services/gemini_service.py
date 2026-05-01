import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3-flash-preview"

def estimate_crop_values(weather, location, crops):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    params = {"key": GEMINI_API_KEY}
    crop_lines = ", ".join(crops)
    prompt = f"""
You are an agriculture advisor for India.

Weather: temperature {weather.get('temperature')} C, humidity {weather.get('humidity')}%, rainfall {weather.get('rainfall') or 0} mm.
Location: {location.get('district')}, {location.get('state')}.
Predicted crops: {crop_lines}.

Return only valid JSON in this format:
{{
  "crops": [
    {{"crop": "crop name", "estimated_value": 2500, "unit": "Rs/quintal"}}
  ],
  "summary": "short farmer-friendly advice under 100 words"
}}

Estimate realistic price values depending on the place and seasons. Prefer crops with better yield and profitability for this location, and sort crops by estimated_value from high to low.
""".strip()

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"},
    }
    response = requests.post(url, params=params, json=payload, timeout=30)
    data = response.json()
    if "candidates" in data:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    return {"crops": [{"crop": crop, "estimated_value": 0, "unit": "Rs/quintal"} for crop in crops], "summary": data.get("error", {}).get("message", "Gemini unavailable.")}
