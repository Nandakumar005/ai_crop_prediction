import requests


def get_location_details(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1,
    }
    headers = {"User-Agent": "ai-crop-recommendation/1.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()

        address = data.get("address", {})
        return {
            "state": address.get("state", ""),
            "district": address.get("state_district") or address.get("county") or "",
        }
    except Exception as e:
        print(f"Location API error: {e}")
        return {
            "state": "",
            "district": "",
        }
