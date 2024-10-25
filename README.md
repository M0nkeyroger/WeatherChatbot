Weather Chatbot
===============

This project is a weather chatbot web application that combines OpenAI's language model with a weather API to provide users with real-time weather information and answer location-based queries. The bot is interactive, responding to user queries with weather details and general conversational abilities, using Flask as the backend.

Table of Contents
-----------------

*   [Features](#features)
*   [Technologies Used](#technologies-used)
*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Usage](#usage)
*   [Environment Variables](#environment-variables)
*   [Screenshots](#screenshots)
*   [License](#license)

Features
--------

*   **Real-Time Weather Updates**: Responds with current weather details based on user location.
*   **Chatbot Conversation**: Uses OpenAI's API for natural language responses to user queries.
*   **Location Flexibility**: Allows users to change the queried location to get updated weather information.
*   **User Interface**: Features a modern, user-friendly interface designed for a conversational experience.

Technologies Used
-----------------

*   **Python**: Backend development and API handling
*   **Flask**: Web framework for routing and API integration
*   **MongoDB**: Database to store user responses
*   **OpenAI API**: Provides natural language responses
*   **WeatherAPI**: Supplies current weather information
*   **HTML/CSS**: Frontend layout and styling
*   **JavaScript**: Manages user interaction and API communication in the UI

Prerequisites
-------------

*   Python 3.7 or higher
*   MongoDB account and database setup
*   OpenAI and WeatherAPI accounts to get respective API keys

Installation
------------

1.  **Clone the Repository**:
    
        git clone https://github.com/M0nkeyroger/WeatherChatbot.git
        cd WeatherChatbot
            
    
2.  **Install Required Packages**:
    
        pip install -r requirements.txt
    
3.  **Set Up Environment Variables**: See [Environment Variables](#environment-variables) section for required variables.

Usage
-----

1.  **Run the Flask Application**:
    
        python main.py
    
2.  Open your browser and navigate to `http://127.0.0.1:5000/` to interact with the chatbot.
3.  **Interacting with the Chatbot**:
    *   **Start**: Type in any greeting or question.
    *   **Weather Updates**: Type a location to get the latest weather information.
    *   **Change Location**: Type “clima” or provide a new location to update the queried weather location.

Environment Variables
---------------------

Create a `.env` file in the root directory with the following details:

    OPENAI_API_KEY=your_openai_api_key
    WEATHER_API_KEY=your_weatherapi_key
    MONGODB_USER=your_mongodb_username
    MONGODB_PASSWORD=your_mongodb_password
    MONGODB_DB=your_database_name
    

Screenshots
-----------

![Weather Chatbot Screenshot](https://github-production-user-asset-6210df.s3.amazonaws.com/79229146/380223801-cf0e8fb8-e4a7-497e-ba35-5af46631b06c.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20241025%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241025T151514Z&X-Amz-Expires=300&X-Amz-Signature=251fe292682049cb24cd576a2975e02c7c9323dd9179a026f0046e81a1d40b5f&X-Amz-SignedHeaders=host)

License
-------

This project is licensed under the MIT License.
