import os
import json
import requests
from dotenv import load_dotenv

def estimate_crop_values(weather, location, crops):
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"
    params = {"key": gemini_api_key}
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
