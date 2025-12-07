import requests

API_KEY = "AIzaSyB5mPXxvTsbLNegWSr_SZKKkFbwBJNR50A"
URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def search_claims(query):
    try:
        params = {
            "query": query,
            "key": API_KEY
        }

        response = requests.get(URL, params=params)
        data = response.json()

        if "claims" in data:
            return data["claims"]
        else:
            return []

    except Exception as e:
        return []
