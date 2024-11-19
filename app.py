from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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

@app.route("/news", methods=["POST","GET"])
def fetch_news():
    # Parse request data
    data = request.get_json()
    data['apiKey']="52414c7d904b41c4b05e263e2f243d08"       
    
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

