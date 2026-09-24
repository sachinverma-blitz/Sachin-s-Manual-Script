import warnings
warnings.filterwarnings("ignore", category=Warning)

import requests
import json
from datetime import datetime
import time

# --- CONFIG ---
API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/tracking/Update_shipment_status"
HEADERS = {"Content-Type": "application/json"}

# --- INPUT ---
awb_user_pairs =[
  {"awb": "BZNYB3719647", "userId": 738}
]
# add more pairs here


# --- STATIC FIELDS ---
base_data = {
    "location": "Bangalore",
    "shipperId": 301,
    "remark": "",
    "shipmentStatus": "Delivered"
}

# --- SEND REQUESTS ---
for pair in awb_user_pairs:
    awb = pair["awb"]
    user_id = pair["userId"]

    payload_data = base_data.copy()
    payload_data.update({
        "awb": awb,
        "userId": user_id,
        "updateTime": datetime.now().strftime("%m/%d/%Y %H:%M")
    })

    payload = [payload_data]

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)

        if response.ok:
            print(f"✅ AWB: {awb} | UserID: {user_id} | Success")
        else:
            print(f"❌ AWB: {awb} | UserID: {user_id} | Failed | {response.status_code} | {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error for AWB {awb}: {e}")

    time.sleep(0.5)

print("🎯 All AWBs processed.")
