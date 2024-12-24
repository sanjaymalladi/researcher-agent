from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from scholarly import scholarly

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API Configurations
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
CORE_API_URL = "https://core.ac.uk/api-v2/articles/search"
CORE_API_KEY = os.getenv("CORE_API_KEY")

# Helper function to fetch papers from Semantic Scholar
def fetch_semantic_scholar(topic, limit):
    headers = {"x-api-key": SEMANTIC_SCHOLAR_API_KEY}
    params = {
        "query": topic,
        "fields": "title,authors,abstract,year,url,isOpenAccess",
        "limit": limit,
    }
    response = requests.get(
        "https://api.semanticscholar.org/graph/v1/paper/search",
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return []

# Helper function to fetch papers from CORE
def fetch_core(topic, limit):
    params = {"q": topic, "apiKey": CORE_API_KEY, "limit": limit}
    response = requests.get(CORE_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return []

# Helper function to fetch papers from Google Scholar
def fetch_google_scholar(topic, limit):
    search_query = scholarly.search_pubs(topic)
    results = []
    for i, paper in enumerate(search_query):
        if i >= limit:
            break
        results.append(
            {
                "title": paper.bib.get("title", "No Title"),
                "authors": paper.bib.get("author", "Unknown").split(", "),
                "abstract": paper.bib.get("abstract", "No Abstract"),
                "year": paper.bib.get("pub_year", "Unknown"),
                "url": paper.bib.get("url", ""),
                "isOpenAccess": False,  # Google Scholar doesn't provide this info
            }
        )
    return results

@app.route("/search", methods=["POST"])
def search_papers():
    data = request.get_json()
    topic = data.get("topic")
    limit = data.get("limit", 10)

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Fetch results from multiple sources
    semantic_results = fetch_semantic_scholar(topic, limit)
    core_results = fetch_core(topic, limit)
    google_scholar_results = fetch_google_scholar(topic, limit)

    # Combine results
    results = semantic_results + core_results + google_scholar_results

    formatted_results = []
    for paper in results:
        formatted_results.append(
            {
                "title": paper.get("title"),
                "authors": paper.get("authors", []),
                "abstract": paper.get("abstract"),
                "year": paper.get("year"),
                "url": paper.get("url"),
                "isOpenAccess": paper.get("isOpenAccess", False),
            }
        )

    return jsonify({"papers": formatted_results})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
