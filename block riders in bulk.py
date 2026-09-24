import requests
import time

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/personnel_status"

data =[ 
   {"rider_id":"24020","node_id":"159"},
{"rider_id":"19127","node_id":"159"},
{"rider_id":"23665","node_id":"159"},
{"rider_id":"13566","node_id":"159"},
{"rider_id":"19671","node_id":"159"},
{"rider_id":"15556","node_id":"159"},
{"rider_id":"15091","node_id":"159"},
{"rider_id":"29985","node_id":"159"},
{"rider_id":"24765","node_id":"159"}
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
        "reason": "Behavioural Issues"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        print(f"Rider {row['rider_id']} | Node {row['node_id']} | {response.status_code} | {response.text}")
    except Exception as e:
        print(f"Error for {row['rider_id']}: {e}")

    time.sleep(0.4)