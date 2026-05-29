import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

POOL_ID = "ap-south-1_2nXMZRCaO"
USERNAME = "8054554044"

ORG_IDS = [
  
239
  ]




for i, org_id in enumerate(ORG_IDS, start=1):
    headers = {
        "pool": POOL_ID,
        "orgId": str(org_id),
        "Content-Type": "application/json"
    }

    payload = {
        "request_type": "delete_user_account",
        "payload": {
            "username": USERNAME
        }
    }

    r = requests.post(API_URL, headers=headers, json=payload)

    if r.status_code == 200:
        print(f"✅ {i}. Deleted {USERNAME} | Org {org_id}")
    else:
        print(f"❌ {i}. Failed | Org {org_id} | {r.text}")

    time.sleep(0.3)
