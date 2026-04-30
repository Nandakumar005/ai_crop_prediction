from pathlib import Path
import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "crop_recommendation_model.pkl"
FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

model = joblib.load(MODEL_PATH)


def predict_top_crops(N, P, K, temp, humidity, ph, rainfall):
    features = pd.DataFrame(
        [[N, P, K, temp, humidity, ph, rainfall]],
        columns=FEATURE_COLUMNS,
    )

    probs = model.predict_proba(features)[0]
    classes = model.classes_
    pairs = list(zip(classes, probs))
    pairs.sort(key=lambda x: x[1], reverse=True)

    return [crop for crop, _ in pairs[:20]]
