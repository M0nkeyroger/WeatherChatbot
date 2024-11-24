import os
import urllib.parse
import requests
from flask import Flask, request, jsonify, render_template, session
import openai
from dotenv import load_dotenv
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Get API keys from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
TIME_API_KEY = os.getenv('TIME_API_KEY')

# Get MongoDB URI from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

# Debugging statement
print(f"Connecting to MongoDB URI: {MONGODB_URI}")

# Ensure API keys are loaded
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set in environment variables.")
if not WEATHER_API_KEY:
    raise ValueError("Error: WEATHER_API_KEY is not set in environment variables.")
if not GEOAPIFY_API_KEY:
    raise ValueError("Error: GEOAPIFY_API_KEY is not set in environment variables.")
if not MONGODB_URI:
    raise ValueError("Error: MONGODB_URI is not set in environment variables.")
if not TIME_API_KEY:
    raise ValueError("Error: TIME_API_KEY is not set in environment variables.")

# Initialize the OpenAI API client with the API key
openai.api_key = OPENAI_API_KEY

# Connect to MongoDB using the provided example
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Select the database and collection
db = client['weather_chatbot_db']
collection = db['user_queries']

# Define the function to save user input
def save_user_input(user_input, bot_response):
    try:
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        db = client['weather_chatbot_db']
        collection = db['user_queries']
        
        document = {
            "user_input": user_input,
            "user_input_timestamp": datetime.now(timezone.utc),
            "bot_response": bot_response,
            "bot_response_timestamp": datetime.now(timezone.utc)
        }
        
        result = collection.insert_one(document)
        print(f"Document inserted with _id: {result.inserted_id}")
    except Exception as e:
        print(f"Error saving user input: {e}")


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Variable to store the last queried location
last_location = "Querétaro"  # Default location

# Variable to store the last fetched weather data
last_weather_data = None

def geocode_location(location_name):
    # Get the GEOAPIFY_API_KEY from environment variables
    GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
    # Debugging statement
    print(f"GEOAPIFY_API_KEY: {GEOAPIFY_API_KEY}")

    # Build the API URL
    api_url = f"https://api.geoapify.com/v1/geocode/search?text={urllib.parse.quote(location_name)}&apiKey={GEOAPIFY_API_KEY}&lang=es"
    print(f"Geocoding API URL: {api_url}")
    # Send the request
    response = requests.get(api_url)
    print(f"Geocoding Response Status Code: {response.status_code}")
    print(f"Geocoding Response Content: {response.content}")

    if response.status_code == 200:
        data = response.json()
        if data['features']:
            # Get the first result
            first_feature = data['features'][0]
            lat = first_feature['geometry']['coordinates'][1]
            lon = first_feature['geometry']['coordinates'][0]
            print(f"Coordinates: {lat}, {lon}")
            return f"{lat},{lon}"
        else:
            print("No features found in geocoding response.")
            return None
    else:
        print("Geocoding API request failed.")
        return None

def fetch_weather(location):
    # Geocode the location to get coordinates
    coordinates = geocode_location(location)
    if not coordinates:
        print("Failed to get coordinates.")
        return None  # Could not geocode the location

    api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={coordinates}&aqi=no&lang=es"
    print(f"Weather API URL: {api_url}")
    response = requests.get(api_url)
    print(f"Weather API Status Code: {response.status_code}")
    print(f"Weather API Response Content: {response.content}")

    if response.status_code != 200 or 'error' in response.json():
        print("Failed to fetch weather data.")
        return None  # Return None if the API request fails

    return response.json()

@app.route("/")
def home():
    return render_template("index.html")  # Ensure you have an index.html file in a templates folder

@app.route("/chat", methods=["POST"])
def chat_with_gpt():
    global last_location, last_weather_data

    user_input = request.json.get("message").strip()
    print(f"User input: {user_input}")

    # Initialize conversation history in session
    if 'conversation_history' not in session:
        session['conversation_history'] = []

    # Convert input to lowercase for comparison
    user_input_lower = user_input.lower()

    # Check if the user wants to change the location
    if user_input_lower in ["cambiar ubicación", "cambiar ubicacion", "cambiar ciudad"]:
        session['awaiting_location'] = True
        session['conversation_history'].append({"role": "user", "content": user_input})
        return jsonify({"response": "Por favor, proporciona una nueva ciudad o ubicación para actualizar el clima."})

    # Check if the bot has asked for a new location previously
    if session.get('awaiting_location', False):
        last_location = user_input.strip().title()  # Update the last queried location
        session['awaiting_location'] = False  # Reset the flag

        # Fetch weather data for the new location
        weather_data = fetch_weather(last_location)
        if (weather_data and "current" in weather_data):
            last_weather_data = weather_data  # Store the last weather data
            response_text = f"Ubicación actualizada a {last_location}. Puedes preguntarme sobre el clima o cualquier otra cosa."
            session['conversation_history'].append({"role": "user", "content": user_input})
            session['conversation_history'].append({"role": "assistant", "content": response_text})
            return jsonify({"response": response_text})
        else:
            response_text = "No se pudo obtener la información del clima para esa ubicación. Por favor, intenta con otra."
            session['conversation_history'].append({"role": "user", "content": user_input})
            session['conversation_history'].append({"role": "assistant", "content": response_text})
            return jsonify({"response": response_text})

    # Check if the user is asking about the weather in a specific location
    match = re.search(r'clima en ([\w\s,áéíóúñü]+)', user_input_lower)
    if match:
        location = match.group(1).strip().title()
        weather_data = fetch_weather(location)
        if weather_data and "current" in weather_data:
            last_location = location
            last_weather_data = weather_data  # Update last weather data
            # Add user input to conversation history
            session['conversation_history'].append({"role": "user", "content": user_input})
            # Get response from ChatGPT
            response_text = get_chatgpt_response(weather_data, user_input)
            session['conversation_history'].append({"role": "assistant", "content": response_text})
            return jsonify({"response": response_text})
        else:
            response_text = f"No se pudo obtener la información del clima para {location}. Por favor, intenta con otra ubicación."
            session['conversation_history'].append({"role": "user", "content": user_input})
            session['conversation_history'].append({"role": "assistant", "content": response_text})
            return jsonify({"response": response_text})

    # Check if the user is asking about the weather generally
    if any(word in user_input_lower for word in ["clima", "tiempo", "temperatura", "pronóstico", "pronostico"]):
        weather_data = fetch_weather(last_location)
        if weather_data and "current" in weather_data:
            last_weather_data = weather_data  # Update last weather data
            # Add user input to conversation history
            session['conversation_history'].append({"role": "user", "content": user_input})
            # Get response from ChatGPT
            response_text = get_chatgpt_response(weather_data, user_input)
            session['conversation_history'].append({"role": "assistant", "content": response_text})
            return jsonify({"response": response_text})
        else:
            response_text = "No se pudo obtener la información del clima. Por favor, asegúrate de haber establecido una ubicación válida."
            session['conversation_history'].append({"role": "user", "content": user_input})
            session['conversation_history'].append({"role": "assistant", "content": response_text})
            return jsonify({"response": response_text})

    # General conversation using OpenAI API
    session['conversation_history'].append({"role": "user", "content": user_input})

    # Build messages for OpenAI API
    messages = [
        {"role": "system", "content": "Eres un asistente virtual amable y servicial que puede proporcionar información sobre el clima y mantener conversaciones generales."}
    ]

    # Include weather context if available
    if last_weather_data:
        weather_description = last_weather_data['current']['condition']['text']
        temperature = last_weather_data['current']['temp_c']
        weather_location = last_weather_data['location']['name']
        weather_context = f"El clima en {weather_location} es {weather_description.lower()} con una temperatura de {temperature}°C."
        messages[0]['content'] += " " + weather_context

    # Add conversation history
    messages += session['conversation_history']

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages[-10:],  # Limit to the last 10 messages to stay within token limits
        max_tokens=150,
        temperature=0.7,
    )

    assistant_reply = response.choices[0].message['content']

    # Add assistant's reply to conversation history
    session['conversation_history'].append({"role": "assistant", "content": assistant_reply})

    # Save the user input and bot response to MongoDB
    save_user_input(user_input, assistant_reply)

    return jsonify({"response": assistant_reply})

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['message']
    
    # Initialize conversation history if not present
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    
    # Append user's message to conversation history
    session['conversation_history'].append({"role": "user", "content": user_input})
    
    # Build messages for OpenAI API
    messages = [
        {
            "role": "system",
            "content": "Eres un asistente virtual amable y servicial que puede proporcionar información sobre el clima y mantener conversaciones generales."
        }
    ]
    
    # Include previous conversation history
    messages += session['conversation_history']
    
    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages[-10:],  # Limit to last 10 messages
        max_tokens=150,
        temperature=0.7,
    )
    
    assistant_reply = response.choices[0].message['content']
    
    # Add assistant's reply to conversation history
    session['conversation_history'].append({"role": "assistant", "content": assistant_reply})
    
    # Save the user input and bot response to MongoDB
    print("Saving to MongoDB...")
    save_user_input(user_input, assistant_reply)
    
    return jsonify({"response": assistant_reply})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    location_data = request.json.get('locationData')

    # Save user query to MongoDB
    try:
        collection.insert_one({
            "message": user_message,
            "timestamp": datetime.now(timezone.utc)
        })
    except Exception as e:
        print(f"Error saving user input: {e}")

    if "hora" in user_message.lower():
        if not location_data:
            return jsonify({"response": "No se ha obtenido la ubicación. Por favor, intenta nuevamente."}), 200
        # Fetch time data from /get_time endpoint
        time_api_url = f"https://timeapi.io/api/Time/current/coordinate?latitude={location_data['latitude']}&longitude={location_data['longitude']}&key={TIME_API_KEY}"
        print(f"Fetching time data from URL: {time_api_url}")  # Logging

        try:
            response = requests.get(time_api_url)
            response.raise_for_status()
            time_data = response.json()
            datetime_iso = time_data.get('dateTime')
            if not datetime_iso:
                print("Time API response does not contain 'dateTime' field.")
                return jsonify({"response": "Error al obtener la hora."}), 500
            print(f"Retrieved datetime: {datetime_iso}")  # Logging
            datetime_obj = datetime.fromisoformat(datetime_iso)
            current_time = datetime_obj.strftime('%H:%M')
            assistant_reply = f"¡Claro! Déjame ver... En este momento son las {current_time}. ¿Hay algo más en lo que pueda ayudarte?"
        except requests.exceptions.RequestException as e:
            print(f"Time API request failed: {e}")  # Logging
            assistant_reply = "Ocurrió un error al obtener la hora. Por favor, intenta nuevamente."
        except Exception as e:
            print(f"Unexpected error: {e}")
            assistant_reply = "Ocurrió un error inesperado. Por favor, intenta nuevamente."

        # Save bot response to MongoDB
        save_user_input(user_message, assistant_reply)
        return jsonify({"response": assistant_reply})

    elif "día" in user_message.lower() or "día" in user_message.lower() or "dia" in user_message.lower():
        if not location_data:
            return jsonify({"response": "No se ha obtenido la ubicación. Por favor, intenta nuevamente."}), 200
        # Fetch time data from /get_time endpoint
        time_api_url = f"https://timeapi.io/api/Time/current/coordinate?latitude={location_data['latitude']}&longitude={location_data['longitude']}&key={TIME_API_KEY}"
        print(f"Fetching time data from URL: {time_api_url}")  # Logging

        try:
            response = requests.get(time_api_url)
            response.raise_for_status()
            time_data = response.json()
            datetime_iso = time_data.get('dateTime')
            if not datetime_iso:
                print("Time API response does not contain 'dateTime' field.")
                return jsonify({"response": "Error al obtener la fecha."}), 500
            print(f"Retrieved datetime: {datetime_iso}")  # Logging
            datetime_obj = datetime.fromisoformat(datetime_iso)
            current_date = datetime_obj.strftime('%A, %d de %B de %Y')
            assistant_reply = f"Hoy es {current_date}. ¿Hay algo más en lo que pueda ayudarte?"
        except requests.exceptions.RequestException as e:
            print(f"Time API request failed: {e}")  # Logging
            assistant_reply = "Ocurrió un error al obtener la fecha. Por favor, intenta nuevamente."
        except Exception as e:
            print(f"Unexpected error: {e}")
            assistant_reply = "Ocurrió un error inesperado. Por favor, intenta nuevamente."

        # Save bot response to MongoDB
        save_user_input(user_message, assistant_reply)
        return jsonify({"response": assistant_reply})

    else:
        # Handle other types of queries using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente virtual amable y servicial que puede proporcionar información sobre el clima y mantener conversaciones generales."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            assistant_reply = response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            assistant_reply = "Ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente."

        # Add assistant's reply to conversation history
        session.setdefault('conversation_history', []).append({"role": "assistant", "content": assistant_reply})

        # Save the user input and bot response to MongoDB
        print("Saving to MongoDB...")
        save_user_input(user_message, assistant_reply)

        return jsonify({"response": assistant_reply})

@app.route('/get_time', methods=['GET'])
def get_time():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    time_api_key = TIME_API_KEY  # Use your API key

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # Corrected Time API URL
    time_api_url = f"https://timeapi.io/api/Time/current/coordinate?latitude={lat}&longitude={lon}&key={time_api_key}"

    print(f"Fetching time data from URL: {time_api_url}")  # Logging

    try:
        response = requests.get(time_api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Time API request failed: {e}")  # Logging
        return jsonify({"error": f"Failed to fetch time data: {e}"}), 500

    time_data = response.json()

    # Extract datetime in ISO format
    datetime_iso = time_data.get('dateTime')
    if not datetime_iso:
        print("Time API response does not contain 'dateTime' field.")  # Logging
        return jsonify({"error": "Invalid response from Time API"}), 500

    print(f"Retrieved datetime: {datetime_iso}")  # Logging

    return jsonify({"datetime": datetime_iso})

def get_chatgpt_response(weather_data, user_question):
    weather_description = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']
    weather_location = weather_data['location']['name']

    # Construct the assistant's message with weather information
    assistant_message = f"El clima actual en {weather_location} es {weather_description.lower()} con una temperatura de {temperature}°C. ¿Hay algo más en lo que pueda ayudarte?"

    return assistant_message

if __name__ == "__main__":
    app.run(debug=True)