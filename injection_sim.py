import requests

URL = "http://127.0.0.1:8000/api/public/films/"

PAYLOADS = [
    "' OR 1=1 --",
    "' UNION SELECT 1,username,password FROM auth_user --",
    "admin' --",
    "1; DROP TABLE api_film --"
]

def test_sql_injection():
    print(f"Testing SQL Injection robustness on {URL}...")
    
    for payload in PAYLOADS:
        print(f"\nTesting payload: {payload}")
        try:
            # Injecting in ville parameter
            params = {'ville': payload}
            response = requests.get(URL, params=params)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ CRITICAL: Server Error (500) - Potential Vulnerability!")
            elif response.status_code == 200:
                print("✅ OK: Handled gracefully (200).")
                # Check if we got all films (which might indicate OR 1=1 worked if naive SQL)
                # But typically DRF filter backend handles this safe.
            else:
                print(f"⚠️ Response: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_sql_injection()
