import joblib
import pandas as pd

model = joblib.load(r"D:\ai crop\crop_recommendation_model.pkl")

def predict_top_crops(N, P, K, temp, humidity, ph, rainfall):
    features = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]])

    probs = model.predict_proba(features)[0]
    classes = model.classes_

    pairs = list(zip(classes, probs))
    pairs.sort(key=lambda x: x[1], reverse=True)

    return [c[0] for c in pairs[:20]]