# 🌾 AI Crop Prediction

An AI-powered web application that recommends the best crops to grow based on real-time weather conditions, soil nutrient levels, and live market prices.

---

## 🚀 Features

- 📍 **Location-aware** — uses your GPS coordinates to fetch live weather data
- 🌡️ **Real-time weather** — temperature, humidity, and rainfall via OpenWeatherMap
- 🧪 **Soil analysis** — takes N, P, K, and pH values as input
- 🤖 **ML-based prediction** — recommends top 5 crops using a trained classification model
- 💰 **Market prices** —  live prices from data.gov mandi price api if failed estimated price (Rs./quintal) for each recommended crop
- 📊 **Visual chart** — bar chart comparing crop prices
- 🧠 **AI advisory** — natural language farming advice powered by Google Gemini

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML Model | scikit-learn (joblib) |
| AI Advisory | Google Gemini 2.0 Flash |
| Weather | OpenWeatherMap API |
|Market data|data.gov api|
| Location | Nominatim (OpenStreetMap) |
| Charts | Matplotlib |
| Frontend | HTML, CSS, JavaScript (Jinja2) |

---

## 📁 Project Structure

```
ai_crop_prediction/
│
├── app.py                  # Flask entry point
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
│
├── models/
│   └── crop_recommendation_model.pkl   # Trained ML model
│
├── services/
│   ├── crop_service.py     # ML prediction logic
│   ├── market_service.py   # Market price estimation
│   ├── weather_data.py     # OpenWeatherMap integration
│   ├── location_service.py # Reverse geocoding
│   └── gemini_service.py   # Gemini AI advisory
│
├── data/
│   └── Crop_recommendation.csv   # Training dataset
│
├── static/
│   └── chart.png           # Generated crop price chart
│
└── templates/
    └── index.html          # Frontend UI
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nandakumar005/ai_crop_prediction.git
cd ai_crop_prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_openweathermap_api_key
GEMINI_API_KEY=your_google_gemini_api_key
MARKET_API_KEY=your_key
```

> Get your OpenWeatherMap key at [openweathermap.org](https://openweathermap.org/api)
> Get your Gemini key at [aistudio.google.com](https://aistudio.google.com)

### 4. Run the app

```bash
python app.py
```

Open your browser at `http://localhost:5000`

---

## 🧪 How It Works

1. User enters **soil values** (N, P, K, pH) and allows **location access**
2. App fetches **live weather data** (temperature, humidity, rainfall) for that location
3. The **ML model** predicts the top 5 most suitable crops
4. **Market prices** live priced are recieved from data.gov if failed it shows estimated fallback price
5. A **bar chart** is generated comparing crop prices
6. Optionally, **Gemini AI** generates a detailed farming advisory

---

## 🌱 Supported Crops

The model is trained to predict among 22 crops:

`rice` · `maize` · `chickpea` · `kidneybeans` · `pigeonpeas` · `mothbeans` · `mungbean` · `blackgram` · `lentil` · `cotton` · `jute` · `coffee` · `apple` · `banana` · `grapes` · `watermelon` · `muskmelon` · `orange` · `papaya` · `coconut` · `mango` · `pomegranate`

---

## 📊 ML Model

- **Dataset:** 2,200 samples, 22 crop classes, 100 samples each
- **Features:** N, P, K, temperature, humidity, pH, rainfall
- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Output:** Top 5 crops ranked by probability

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the main UI |
| POST | `/analyze` | Returns top crops, weather, market data, and chart |
| POST | `/gemini_summary` | Returns AI-generated farming advisory |

### `/analyze` request body

```json
{
  "lat": ,
  "lon":,
  "N":,
  "P": ,
  "K": ,
  "ph": 
}
```
---
## IMPORTANT NOTE⚠️
The data.gov api does not work most of the I tried almost everyway I know I cannot fix or find alternative solution. 
Iam open to any solution

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Nandakumar D**
- GitHub: [@Nandakumar005](https://github.com/Nandakumar005)
- LinkedIn: [nanda-kumar-d-2325a5326](https://linkedin.com/in/nanda-kumar-d-2325a5326)
