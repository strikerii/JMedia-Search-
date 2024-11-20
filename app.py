from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_news_by_topic(params):
    url = "https://newsapi.org/v2/everything"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article for article in articles if article.get("title") != "[Removed]"]
    else:
        return {
            "error": f"Error {response.status_code}: Unable to fetch articles.",
            "details": response.text,
        }

@app.route("/news", methods=["POST", "GET"])
def fetch_news():
    # Parse request data
    data = request.get_json()

    # Add API key from .env
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return jsonify({"error": "API key is missing or not configured."}), 500
    
    data['apiKey'] = api_key

    # Validate inputs
    if not data:
        return jsonify({"error": "Topic is required"}), 400

    # Fetch news using the params
    result = get_news_by_topic(data)

    if isinstance(result, list):  # Successful response
        return jsonify({"articles": result})
    else:  # Error occurred
        return jsonify(result), 500

if __name__ == "__main__":
    app.run(debug=True)
