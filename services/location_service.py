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

    response = requests.get(url, params=params, headers=headers, timeout=20)
    data = response.json()

    if response.status_code != 200:
        raise Exception(
            f"Error fetching location data ({response.status_code}): {data.get('error', 'Unknown error')}"
        )

    address = data.get("address", {})
    return {
        "state": address.get("state", ""),
        "district": address.get("state_district") or address.get("county") or "",
    }
