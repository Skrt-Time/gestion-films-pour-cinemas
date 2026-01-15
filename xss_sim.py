import requests

URL = "http://127.0.0.1:8000/api/public/films/"

XSS_PAYLOAD = "<script>alert('XSS')</script>"

def test_xss():
    print(f"Testing XSS robustness on {URL}...")
    
    # Test Reflected XSS in Search
    print(f"\nTesting Reflected XSS in Ville param: {XSS_PAYLOAD}")
    params = {'ville': XSS_PAYLOAD}
    try:
        response = requests.get(URL, params=params)
        print(f"Status Code: {response.status_code}")
        
        # Check if the payload is reflected efficiently
        # Note: In a JSON API, it is usually returned as a string literal.
        # The specific vulnerability is if the frontend renders this without escaping.
        # The backend should ideally not store it or sanitize it, but mostly libraries handle escaping.
        
        if XSS_PAYLOAD in response.text:
             print("ℹ️ Payload found in response text (Normal for JSON APIs, client must escape).")
        else:
             print("✅ Payload not found directly in response (filtered or no results).")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_xss()
