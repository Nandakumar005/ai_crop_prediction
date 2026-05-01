import os
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template, request

from services.crop_service import predict_top_crops
from services.gemini_service import estimate_crop_values
from services.location_service import get_location_details
from services.weather_data import get_weather_data

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
    n_value = float(data["N"])
    p_value = float(data["P"])
    k_value = float(data["K"])
    ph_value = float(data["ph"])

    weather = get_weather_data(lat, lon)
    location = get_location_details(lat, lon)
    rainfall = weather["rainfall"] or 100
    crops = predict_top_crops(
        n_value,
        p_value,
        k_value,
        weather["temperature"],
        weather["humidity"],
        ph_value,
        rainfall,
    )[:5]
    gemini_result = estimate_crop_values(weather, location, crops)
    chart_url = generate_value_chart(gemini_result["crops"])

    result = {
        "weather": weather,
        "location": location,
        "crops": gemini_result["crops"],
        "summary": gemini_result["summary"],
        "chart_url": chart_url,
    }
    return jsonify(result)


def generate_value_chart(crops):
    names = [crop["crop"].title() for crop in crops if crop.get("estimated_value")]
    values = [crop["estimated_value"] for crop in crops if crop.get("estimated_value")]

    plt.figure(figsize=(8, 4.5))
    if names and values:
        bars = plt.bar(names, values, color="green")
        plt.ylabel("Estimated value (Rs./quintal)")
        plt.xlabel("Crop")
        plt.title(" Estimated Crop Values")
        plt.xticks(rotation=20, ha="right")
        for bar, value in zip(bars, values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.0f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )
    else:
        plt.text(0.5, 0.5, "No estimated values available", ha="center", va="center", fontsize=14)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(CHART_PATH, dpi=140)
    plt.close()
    return f"/static/chart.png?t={int(time.time())}"
if __name__ == "__main__":
    app.run(debug=True)
