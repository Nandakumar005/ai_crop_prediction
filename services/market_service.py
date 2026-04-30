import os
from pathlib import Path
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

MARKET_API_KEY = os.getenv("MARKET_API_KEY")
if not MARKET_API_KEY:
    raise RuntimeError("MARKET_API_KEY is not set in .env")


def get_market_price(commodity=None, state=None, district=None, market=None, limit=10):
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

    return data.get("records", [])


def get_best_price(commodity, state=None, district=None):
    records = get_market_price(
        commodity=commodity.title(),
        state=state,
        district=district,
        limit=50,
    )

    prices = []
    for record in records:
        value = record.get("modal_price") or record.get("Modal_Price")
        if value is None:
            continue
        try:
            prices.append(float(value))
        except (TypeError, ValueError):
            continue

    return max(prices, default=0)
