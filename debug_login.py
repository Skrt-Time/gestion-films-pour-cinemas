import requests

URL = "http://127.0.0.1:8000/login/"

try:
    response = requests.get(URL)
    if "Propri" in response.text:
        print("FOUND 'Propri' in content!")
        idx = response.text.find("Propri")
        print(response.text[idx-100:idx+100])
    else:
        print("NOT FOUND 'Propri'")
except Exception as e:
    print(e)
