import requests
import time

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/personnel_status"

data =[ 
    {"rider_id":"25369","node_id":"125"},
{"rider_id":"27172","node_id":"311"},
{"rider_id":"25387","node_id":"84"},
{"rider_id":"27868","node_id":"125"},
{"rider_id":"28169","node_id":"84"},
{"rider_id":"27016","node_id":"125"},
{"rider_id":"25028","node_id":"84"},
{"rider_id":"28036","node_id":"311"},
{"rider_id":"27781","node_id":"125"},
{"rider_id":"27312","node_id":"325"},
{"rider_id":"24411","node_id":"84"}
]

for row in data:

    headers = {
        "node_id": row["node_id"],
        "Content-Type": "application/json",
        "Name": "Sachin"
    }

    payload = {
        "riderId": [row["rider_id"]],
        "status": "BLACKLISTED",
        "reason": "fraud theft cases"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        print(f"Rider {row['rider_id']} | Node {row['node_id']} | {response.status_code} | {response.text}")
    except Exception as e:
        print(f"Error for {row['rider_id']}: {e}")

    time.sleep(0.4)