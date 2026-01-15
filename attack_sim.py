import requests
import time
import threading

URL = "http://127.0.0.1:8000/api/public/films/"
COUNT = 0
LOCK = threading.Lock()

def send_request():
    global COUNT
    try:
        response = requests.get(URL)
        with LOCK:
            COUNT += 1
            if response.status_code == 429:
                print(f"[{COUNT}] Limit reached! Status: {response.status_code}")
                return True
            elif response.status_code == 200:
                pass
                # print(f"[{COUNT}] OK")
            else:
                print(f"[{COUNT}] Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    return False

def start_attack():
    print(f"Starting throttling test on {URL}...")
    threads = []
    # Send 500 requests (limit should be 100/day for anon)
    for i in range(200):
        t = threading.Thread(target=send_request)
        threads.append(t)
        t.start()
        time.sleep(0.01) # Small delay to not crash the script itself
    
    for t in threads:
        t.join()

    print("Attack simulation finished.")

if __name__ == "__main__":
    start_attack()
