import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

# Sample weather data for practice
data = {
    "humidity": [
        30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
        32, 42, 52, 62, 72, 38, 48, 58, 68, 78
    ],
    "wind_speed": [
        5, 8, 10, 12, 7, 9, 11, 6, 8, 10,
        7, 9, 6, 12, 11, 5, 8, 10, 7, 9
    ],
    "temperature": [
        35, 34, 33, 31, 30, 29, 28, 27, 26, 25,
        34, 32, 30, 28, 26, 33, 31, 29, 27, 24
    ]
}

df = pd.DataFrame(data)

X = df[["humidity", "wind_speed"]]
y = df["temperature"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/weather_model.pkl")

print("Weather prediction model trained successfully!")
print("Mean Absolute Error:", round(error, 2), "°C")

predicted_temp = model.predict(
    pd.DataFrame([{"humidity": 60, "wind_speed": 10}])
)

print("Example predicted temperature:",
      round(predicted_temp[0], 2), "°C")