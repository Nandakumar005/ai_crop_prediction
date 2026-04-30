from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "Crop_recommendation.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "crop_recommendation_model.pkl"

data = pd.read_csv(DATA_PATH)

X = data.drop("label", axis=1)
y = data["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, MODEL_PATH)
print("Model trained & saved")
