import requests

URL = "http://127.0.0.1:8000/api/public/films/"

try:
    print(f"Fetching {URL}...")
    response = requests.get(URL)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}...") # Print start of content
except Exception as e:
    print(f"Error: {e}")
