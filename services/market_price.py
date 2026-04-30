import os
from pathlib import Path
import requests
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

MARKET_API_KEY = os.getenv("MARKET_API_KEY")
if not MARKET_API_KEY:
    raise RuntimeError("MARKET_API_KEY is not set in .env")

def get_market_price(commodity=None, state=None, district=None, market=None, limit=10):
    """
    Fetch market price data from data.gov.in API.

    Parameters:
    - commodity: Name of the commodity (e.g., 'Onion')
    - state: State name
    - district: District name
    - market: Market name
    - limit: Number of records to fetch (default 10)

    Returns:
    List of market price records.
    """
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": MARKET_API_KEY,
        "format": "json",
        "limit": limit,
    }
    if commodity:
        params["filters[commodity]"] = commodity
    if state:
        params["filters[state]"] = state
    if district:
        params["filters[district]"] = district
    if market:
        params["filters[market]"] = market

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception(
            f"Error fetching market price data ({response.status_code}): {data.get('message', 'Unknown error')}"
        )

    # Assuming the API returns records in 'records' key
    records = data.get("records", [])
    return records

# Example usage
if __name__ == "__main__":
    prices = get_market_price(commodity="Onion", limit=5)
    for price in prices:
        print(price)