import requests
import time

# API URL
API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

# Common headers (orgId will change dynamically)
COMMON_HEADERS = {
    "pool": "ap-south-1_2nXMZRCaO",
    "Content-Type": "application/json"
}

# Payload (same for all)
payload = {
    "request_type": "change_user_permission",
    "payload": {
        "username": "9352146065",
        "group_ids": ["City Head"],
        "type": "REPLACE"
    }
}

# List of org IDs (add your bulk org IDs here)
org_ids = [
314,
304,
255,
194,
159,
156,
118,
114,
113]   # <-- update this list

# Loop through each org ID
for org_id in org_ids:
    headers = COMMON_HEADERS.copy()
    headers["orgId"] = str(org_id)

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        print(f"Org ID: {org_id} | Status: {response.status_code} | Response: {response.text}")

    except Exception as e:
        print(f"Org ID: {org_id} | Error: {str(e)}")

    time.sleep(1)  # to avoid rate limiting