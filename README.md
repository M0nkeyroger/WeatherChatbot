<h1>Weather Chatbot</h1>

<p>This project is a weather chatbot web application that combines OpenAI's language model with a weather API to provide users with real-time weather information and answer location-based queries. The bot is interactive, responding to user queries with weather details and general conversational abilities, using Flask as the backend.</p>

<h2>Table of Contents</h2>
<ul>
  <li><a href="#features">Features</a></li>
  <li><a href="#technologies-used">Technologies Used</a></li>
  <li><a href="#prerequisites">Prerequisites</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#environment-variables">Environment Variables</a></li>
  <li><a href="#screenshots">Screenshots</a></li>
  <li><a href="#license">License</a></li>
</ul>

<h2 id="features">Features</h2>
<ul>
  <li><strong>Real-Time Weather Updates</strong>: Responds with current weather details based on user location.</li>
  <li><strong>Chatbot Conversation</strong>: Uses OpenAI's API for natural language responses to user queries.</li>
  <li><strong>Location Flexibility</strong>: Allows users to change the queried location to get updated weather information.</li>
  <li><strong>User Interface</strong>: Features a modern, user-friendly interface designed for a conversational experience.</li>
</ul>

<h2 id="technologies-used">Technologies Used</h2>
<ul>
  <li><strong>Python</strong>: Backend development and API handling</li>
  <li><strong>Flask</strong>: Web framework for routing and API integration</li>
  <li><strong>MongoDB</strong>: Database to store user responses</li>
  <li><strong>OpenAI API</strong>: Provides natural language responses</li>
  <li><strong>WeatherAPI</strong>: Supplies current weather information</li>
  <li><strong>HTML/CSS</strong>: Frontend layout and styling</li>
  <li><strong>JavaScript</strong>: Manages user interaction and API communication in the UI</li>
</ul>

<h2 id="prerequisites">Prerequisites</h2>
<ul>
  <li>Python 3.7 or higher</li>
  <li>MongoDB account and database setup</li>
  <li>OpenAI and WeatherAPI accounts to get respective API keys</li>
</ul>

<h2 id="installation">Installation</h2>
<ol>
  <li><strong>Clone the Repository</strong>:
    <pre><code>git clone https://github.com/M0nkeyroger/WeatherChatbot.git
cd WeatherChatbot
    </code></pre>
  </li>
  <li><strong>Install Required Packages</strong>:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Set Up Environment Variables</strong>: See <a href="#environment-variables">Environment Variables</a> section for required variables.</li>
</ol>

<h2 id="usage">Usage</h2>
<ol>
  <li><strong>Run the Flask Application</strong>:
    <pre><code>python main.py</code></pre>
  </li>
  <li>Open your browser and navigate to <code>http://127.0.0.1:5000/</code> to interact with the chatbot.</li>
  <li><strong>Interacting with the Chatbot</strong>:
    <ul>
      <li><strong>Start</strong>: Type in any greeting or question.</li>
      <li><strong>Weather Updates</strong>: Type a location to get the latest weather information.</li>
      <li><strong>Change Location</strong>: Type “clima” or provide a new location to update the queried weather location.</li>
    </ul>
  </li>
</ol>

<h2 id="environment-variables">Environment Variables</h2>
<p>Create a <code>.env</code> file in the root directory with the following details:</p>

<pre><code>OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_weatherapi_key
MONGODB_USER=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password
MONGODB_DB=your_database_name
</code></pre>

<h2 id="screenshots">Screenshots</h2>
<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/79229146/380223801-cf0e8fb8-e4a7-497e-ba35-5af46631b06c.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20241025%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241025T151514Z&X-Amz-Expires=300&X-Amz-Signature=251fe292682049cb24cd576a2975e02c7c9323dd9179a026f0046e81a1d40b5f&X-Amz-SignedHeaders=host" alt="Weather Chatbot Screenshot" />

<h2 id="license">License</h2>
<p>This project is licensed under the MIT License.</p>
