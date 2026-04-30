from crop_prediction import predict_top_crops
from weather_data import get_weather_data
N = 90
P = 40 
k=50
ph = 6.5
lat = 28.7041
lon = 77.1025
weather = get_weather_data(lat, lon)
temp = weather["temperature"]
humidity = weather["humidity"]
rainfall = weather["rainfall"] if weather["rainfall"] is not None else 0
top_crops = predict_top_crops(N, P, k, temp, humidity, ph, rainfall)
print("Top 5 crop recommendations:")
for crop in top_crops:
    print(f"- {crop}")