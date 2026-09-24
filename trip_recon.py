import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/collect_FD"

HEADERS = {
    "node_id": "387",
    "name": "Hemanth",
    "Content-Type": "application/json"
}

TRIP_IDS = [


50401620,
50405914
]

for trip_id in TRIP_IDS:
    payload = {
        "tripId": trip_id,
        "status": "COLLECT"
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        print(f"Trip ID: {trip_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 50)

    except Exception as e:
        print(f"Error processing {trip_id}: {e}")

    # Sleep for 2 seconds before next request
    time.sleep(0.3)

print("All requests completed.")