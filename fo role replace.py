import requests
import json

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

ORG_IDS = 180,239,112,238,156,108,127,118,113,160,103,194,111,115,183

    # Add more org IDs here


USERNAME = "9142120512"
GROUP_NAME = "City Head"

for org_id in ORG_IDS:
    headers = {
        "pool": "ap-south-1_2nXMZRCaO",
        "orgId": str(org_id),
        "username": "Mohammed Ismail",
        "Content-Type": "application/json"
    }

    payload = {
        "request_type": "change_user_permission",
        "payload": {
            "username": USERNAME,
            "group_ids": [GROUP_NAME],
            "type": "REPLACE"
        }
    }

    try:
        response = requests.post(
            URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"Org ID: {org_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 60)

    except Exception as e:
        print(f"Org ID: {org_id} -> Error: {e}")