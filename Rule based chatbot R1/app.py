import requests
import re
from flask import Flask, render_template, request

app = Flask(__name__)

# OpenWeatherMap API Key (Replace with your key)
API_KEY = "2bf6f4b1430957a9ba88ba384d473887"

# Store chat history
chat_history = []

# Function to fetch real-time weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        return temp, humidity, description
    else:
        return None, None, "Sorry, I couldn't fetch the weather. Please check the city name."

# Function to suggest crops based on weather
def suggest_crops(temp, humidity):
    if temp > 30 and humidity < 40:
        return "🌾 Hot and dry climate detected. Suitable crops: Millet, Sorghum, Maize, Cotton."
    elif 25 <= temp <= 30 and humidity > 50:
        return "🌴 Warm and humid climate detected. Suitable crops: Rice, Sugarcane, Banana, Coconut."
    elif 15 <= temp < 25 and 40 <= humidity <= 60:
        return "🌻 Moderate climate detected. Suitable crops: Wheat, Barley, Chickpeas, Sunflower."
    elif temp < 15:
        return "🍏 Cold climate detected. Suitable crops: Apples, Peas, Mustard, Carrots."
    else:
        return "🌿 Climate conditions are uncertain. Please consult an agricultural expert."

# Rule-Based Chatbot Responses
def get_response(user_input):
    user_input = user_input.lower()

    if re.search(r"hello|hi|hey", user_input):
        return "👋 Hello! I'm your Weather and Crop Advisor. Ask me about the weather or suitable crops."

    elif re.search(r"weather in (.+)", user_input):
        city = re.search(r"weather in (.+)", user_input).group(1)
        temp, humidity, description = get_weather(city)

        if temp is not None:
            weather_info = f"🌤️ The current weather in {city} is {description} with a temperature of {temp}°C and humidity of {humidity}%."
            crop_suggestion = suggest_crops(temp, humidity)
            return f"{weather_info}\n{crop_suggestion}"
        else:
            return "❌ Sorry, I couldn't fetch the weather. Please check the city name."

    elif re.search(r"best crops for (Summer|winter|rainy|autum)", user_input):
        if "hot" in user_input:
            return "🔥 For hot weather, grow Millet, Sorghum, Maize, or Cotton."
        elif "cold" in user_input:
            return "❄️ For cold weather, grow Apples, Peas, Mustard, or Carrots."
        elif "humid" in user_input:
            return "🌊 For humid weather, grow Rice, Sugarcane, Banana, or Coconut."
        elif "moderate" in user_input:
            return "🌥️ For moderate weather, grow Wheat, Barley, Chickpeas, or Sunflower."
        
    elif re.search(r"bye|thanks|thank you", user_input):
        return "👋 Ohh its my pleasure if you have further queries Ask me."

    else:
        return "🤖 I can provide weather updates and suggest crops. Try asking 'Weather in Mumbai' or 'Best crops for hot weather'."

# Flask route for chatbot
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = get_response(user_input)

        # Store chat history
        chat_history.append({"user": user_input, "bot": bot_response})

    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
