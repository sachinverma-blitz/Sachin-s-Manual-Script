import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/personnel_status"

HEADERS = {
    "node_id": "310",
    "Content-Type": "application/json",
    "Name": "Sachin"
}

# Rider IDs to BLOCK
rider_ids = [



 24127,
  25370,
  41928,
  39928,
  40253,
  41722,
  24863,
  27086


]

for rider_id in rider_ids:
    payload = {
        "riderId": [rider_id],
        "status": "BLACKLISTED",   # 🔴 changed here
        "reason": "Defaulters"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)

        print(f"Rider ID: {rider_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 50)

        time.sleep(0.00001)

    except Exception as e:
        print(f"Error for Rider {rider_id}: {e}")