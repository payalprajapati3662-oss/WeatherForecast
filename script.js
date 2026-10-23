const searchBtn = document.getElementById("searchBtn");
const cityInput = document.getElementById("city");
const message = document.getElementById("message");

searchBtn.addEventListener("click", getWeather);

cityInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        getWeather();
    }
});

async function getWeather() {
    const city = cityInput.value.trim();

    if (city === "") {
        message.textContent = "Please enter a city name.";
        return;
    }

    message.textContent = "Getting weather data...";

    try {
        // Get current weather for the entered city
        const weatherResponse = await fetch(
            `https://wttr.in/${encodeURIComponent(city)}?format=j1`
        );

        if (!weatherResponse.ok) {
            throw new Error("Weather data unavailable");
        }

        const weatherData = await weatherResponse.json();
        const current = weatherData.current_condition[0];

        const humidity = Number(current.humidity);
        const windSpeed = Number(current.windspeedKmph);

        // Send weather information to our ML model
        message.textContent = "Predicting temperature...";

        const predictionResponse = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                humidity: humidity,
                wind_speed: windSpeed
            })
        });

        if (!predictionResponse.ok) {
            throw new Error("ML prediction failed");
        }

        const prediction = await predictionResponse.json();

        document.getElementById("cityName").textContent = city;

        document.getElementById("temperature").textContent =
                   "Actual: " + current.temp_C + " °C";

        const predictionText = document.createElement("p");
        predictionText.textContent =
        "ML Predicted: " + prediction.predicted_temperature + " °C";

        const oldPrediction = document.getElementById("prediction");
        if (oldPrediction) oldPrediction.remove();

        predictionText.id = "prediction";
        document.getElementById("weather").appendChild(predictionText);

        document.getElementById("condition").textContent =
            "Current condition: " + current.weatherDesc[0].value;

        document.getElementById("humidity").textContent =
            "Humidity: " + humidity + "%";

        document.getElementById("wind").textContent =
            "Wind Speed: " + windSpeed + " km/h";

        message.textContent = "ML prediction completed!";

    } catch (error) {
        message.textContent =
            "Unable to get data. Check your internet or Flask server.";
    }
}