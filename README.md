# Weather Chatbot 🌦️🤖

A friendly virtual assistant that provides real-time weather information and general conversation capabilities using natural language processing.

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [License](#license)

## ✨ Features

- **Real-Time Weather Updates**: Fetches current weather data for user-specified locations.
- **Natural Language Processing**: Uses OpenAI API for generating human-like responses.
- **Location Services**: Converts city names into coordinates using Geoapify API.
- **Time Information**: Provides current time for specified locations.
- **Conversation History**: Remembers previous interactions during the session.
- **Error Handling**: Provides meaningful error messages for failed API requests or invalid inputs.
- **Database Integration**: Stores user queries and bot responses in MongoDB for future reference.

## 🛠️ Technologies Used

- **Python 3.7+**: Backend development and API handling.
- **Flask**: Web framework for routing and API integration.
- **MongoDB Atlas**: Database to store user responses.
- **OpenAI API**: Provides natural language responses.
- **Geoapify API**: Geocoding service to convert city names into coordinates.
- **Weather API**: Fetches real-time weather data.
- **Time API**: Retrieves current time information for locations.
- **HTML/CSS/JavaScript**: Frontend development for the user interface.

## 📋 Prerequisites

- **Python 3.7+**
- **MongoDB Atlas Account**
- **API Keys** for:
  - OpenAI
  - Geoapify
  - Weather API
  - Time API

## 🚀 Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/weather-chatbot.git
    cd weather-chatbot
    ```

2. **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project root directory.
   - Add the following variables with your actual API keys and MongoDB URI:
     ```dotenv
     OPENAI_API_KEY=your_openai_api_key
     GEOAPIFY_API_KEY=your_geoapify_api_key
     WEATHER_API_KEY=your_weather_api_key
     TIME_API_KEY=your_time_api_key
     MONGODB_URI=your_mongodb_connection_uri
     ```

## ⚙️ Configuration

- **.env File**: Ensure all necessary API keys and MongoDB credentials are correctly set in the `.env` file.
- **Flask Secret Key**: Replace `'your_secret_key_here'` in `main.py` with a secure secret key for session management.

## 📖 Usage

1. **Run the Application**
    ```bash
    python main.py
    ```

2. **Access the Chatbot Interface**
   - Open your web browser and navigate to `http://localhost:5000`.

3. **Interact with the Chatbot**
   - Ask about the weather in a specific city:
     - *"¿Cuál es el clima en Madrid?"*
   - Ask for the current time in a city:
     - *"¿Qué hora es en Tokio?"*
   - Engage in general conversation.

## 📸 Screenshots


![Screenshot 2024-11-24 065805](https://github.com/user-attachments/assets/ba3f3945-1937-4666-a9e0-0c167c4c66c5)
*Figure 1: The chatbot interface providing weather information.*

## 🗄️ Database Setup (MongoDB Atlas)

- **Create a MongoDB Atlas Account**
  - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
- **Set Up a New Cluster**
  - Follow the instructions to create a free cluster.
- **Get Your Connection URI**
  - Replace `your_mongodb_connection_uri` in the `.env` file with your actual URI.

## 🤝 Contributing

1. **Fork the Repository**
2. **Create a New Branch**
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Commit Your Changes**
    ```bash
    git commit -m "Add your message"
    ```
4. **Push to the Branch**
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Open a Pull Request**

## 📄 License

- This project is licensed under the [MIT License](LICENSE).

## 📧 Contact

- For issues, please open an issue on the GitHub repository.
- For other inquiries, contact [monkeyroger2@gmail.com](mailto:monkeyroger2@gmail.com).

