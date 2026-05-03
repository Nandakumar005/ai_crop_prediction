import os
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template, request

from services.crop_service import predict_top_crops
from services.gemini_service import get_gemini_summary
from services.location_service import get_location_details
from services.weather_data import get_weather_data
from services.market_service import get_live_market_data

CHART_PATH = "static/chart.png"

app = Flask(__name__)
os.makedirs("static", exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    lat = float(data["lat"])
    lon = float(data["lon"])
    n = float(data["N"])
    p = float(data["P"])
    k = float(data["K"])
    ph = float(data["ph"])

    weather = get_weather_data(lat, lon)
    location = get_location_details(lat, lon)

    temp = weather["temperature"] if weather["temperature"] is not None else 25
    hum = weather["humidity"] if weather["humidity"] is not None else 60
    rain = weather["rainfall"] or 100

    crops = predict_top_crops(n, p, k, temp, hum, ph, rain, top_n=5)
    market = get_live_market_data(crops)
    chart = make_chart(market)

    return jsonify({
        "weather": weather,
        "location": location,
        "crops": market,
        "chart_url": chart,
    })


@app.route("/gemini_summary", methods=["POST"])
def gemini_summary():
    data = request.json
    weather = data.get("weather", {})
    location = data.get("location", {})
    crops = data.get("crops", [])
    soil_npk = data.get("soil_npk", {})
    farm_info = data.get("farm_info", {})

    result = get_gemini_summary(weather, location, crops, soil_npk, farm_info)
    return jsonify(result)


def make_chart(crops):
    names = [c["crop"].title() for c in crops if c.get("estimated_value")]
    values = [c["estimated_value"] for c in crops if c.get("estimated_value")]

    plt.figure(figsize=(8, 4.5))
    if names and values:
        bars = plt.bar(names, values, color="green")
        plt.ylabel("Estimated price (Rs./quintal)")
        plt.xlabel("Crop")
        plt.title("Top crops by estimated price")
        plt.xticks(rotation=20, ha="right")
        for bar, val in zip(bars, values):
            plt.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{val:.0f}", ha="center", va="bottom", fontsize=9,
            )
    else:
        plt.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(CHART_PATH, dpi=140)
    plt.close()
    return f"/static/chart.png?t={int(time.time())}"


if __name__ == "__main__":
    app.run(debug=True)
