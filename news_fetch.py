import requests

NEWSAPI_KEY = "a1f0768343ed4d999fd0f135a3d16cb0"

def fetch_articles(query):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": 10,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWSAPI_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get("articles", [])
