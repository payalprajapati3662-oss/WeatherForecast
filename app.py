from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("model/weather_model.pkl")


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    humidity = float(data["humidity"])
    wind_speed = float(data["wind_speed"])

    features = pd.DataFrame([{
        "humidity": humidity,
        "wind_speed": wind_speed
    }])

    temperature = model.predict(features)[0]

    return jsonify({
        "predicted_temperature": round(float(temperature), 2)
    })


if __name__ == "__main__":
    app.run(debug=True)