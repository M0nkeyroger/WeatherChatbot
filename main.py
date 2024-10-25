import os
import urllib.parse
import requests
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys and MongoDB URI from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DB = os.getenv("MONGODB_DB")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# URL-encode the password
MONGODB_PASSWORD = urllib.parse.quote_plus(MONGODB_PASSWORD)

# Create the MongoDB URI
mongodb_uri = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@openaibot.xmfvs.mongodb.net/{MONGODB_DB}?retryWrites=true&w=majority"

# Initialize the OpenAI API client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Create a MongoDB client
mongo_client = MongoClient(mongodb_uri)
db = mongo_client[MONGODB_DB]
responses_collection = db.saved_responses  # Collection to store saved responses

# Initialize the Flask application
app = Flask(__name__)

# Variable to store the last queried location
last_location = "Querétaro"  # Default location

@app.route("/")
def home():
    return render_template("index.html")  # Ensure you have an index.html file in a templates folder

def fetch_weather(location):
    api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return None  # Return None if the API request fails
    
    return response.json()

def get_chatgpt_response(weather_data, user_question):
    weather_description = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']

    # Construct the prompt for OpenAI
    prompt = f"""
    Eres un asistente inteligente. Aquí hay información sobre el clima:
    Descripción: {weather_description}
    Temperatura: {temperature}°C

    El usuario ha preguntado: "{user_question}"

    Responde de manera adecuada a la pregunta del usuario basada en la información del clima, pero también permite discusiones generales.
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )

    # Correctly access the response content
    return response.choices[0].message.content  # Access the content correctly

@app.route("/chat", methods=["POST"])
def chat_with_gpt():
    global last_location  # Use the global variable to track the last queried location
    user_input = request.json.get("message").strip().lower()

    # Debugging log: Check what user input is received
    print(f"User input: {user_input}")

    # Introduce the bot on the first interaction
    if user_input == "":
        return jsonify({"response": "¡Hola! Soy tu asistente virtual. Por favor, proporciona una ubicación o un código postal para que pueda darte la información del clima. Puedes escribir 'clima' en cualquier momento para cambiar la ubicación."})

    # Check if the user specifically asks for 'clima'
    if user_input == "clima":
        return jsonify({"response": "Por favor, proporciona una ubicación o un código postal para el clima."})

    # Check if the user asks "clima?" at any point
    if "clima?" in user_input:
        weather_data = fetch_weather(last_location)

        if weather_data and "current" in weather_data:
            weather_description = weather_data['current']['condition']['text']
            temperature = weather_data['current']['temp_c']
            response = f"El clima actual en {last_location} es {weather_description.lower()} con una temperatura de {temperature}°C. ¿Hay algo más en lo que te pueda ayudar o hablar?"
            return jsonify({"response": response})
        else:
            return jsonify({"response": "No se pudo obtener la información del clima. Inténtalo de nuevo."})

    # Use the user's input directly as the location
    last_location = user_input  # Update the last queried location
    weather_data = fetch_weather(last_location)

    if weather_data and "current" in weather_data:
        # Get response from ChatGPT
        response = get_chatgpt_response(weather_data, user_input)
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No se pudo obtener la información del clima. Inténtalo de nuevo."})

if __name__ == "__main__":
    app.run(debug=True)