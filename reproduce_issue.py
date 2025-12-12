
import urllib.request
import urllib.error
import json

BASE_URL = "http://127.0.0.1:8000"

def post_json(url, data):
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data).encode('utf-8')
    req.add_header('Content-Length', len(jsondata))
    
    try:
        response = urllib.request.urlopen(req, jsondata)
        return response.getcode(), response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        return 0, str(e.reason)

def test_create_film():
    print("--- Testing Film Creation ---")
    url = f"{BASE_URL}/api/cinemas/1/films/"
    data = {
        "titre": "Test Film Agent",
        "realisateur": "Agent Smith",
        "acteurs": "Keanu Reeves",
        "duree": "2h 00min",
        "age_min": "12+",
        "description": "A test film created by the agent.",
        "image_url": "http://example.com/poster.jpg"
    }
    status, response = post_json(url, data)
    print(f"Status: {status}")
    print(f"Response: {response}")
    
    if status == 201:
        return True, json.loads(response)
    return False, None

def test_create_programmation(film_id):
    print("\n--- Testing Programmation Creation ---")
    url = f"{BASE_URL}/api/cinemas/1/films/{film_id}/programmations/"
    data = {
        "date_debut": "2025-01-01",
        "date_fin": "2025-01-31",
        "jours": "Lundi,Mardi",
        "heure": "20:00:00"
    }
    status, response = post_json(url, data)
    print(f"Status: {status}")
    print(f"Response: {response}")
    return status == 201

if __name__ == "__main__":
    success_film, film_data = test_create_film()
    if success_film:
        film_id = film_data['id']
        test_create_programmation(film_id)
    else:
        print("Skipping Programmation test due to film creation failure.")
