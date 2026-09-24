import requests
import time

# List of AWBs to update
awb_list = [
  

"GS5395416781",
"GS2472741452",
"GS5407447440"
]

# Add more AWBs here


# Single status for all
shipment_status = "Delivered"  # Change to desired status (e.g., "Failed Delivered", "Picked-up", etc.)

# API endpoint
url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/tracking/Delete_tracking"

# Headers
headers = {
    "token": "delete-token-1290",
    "Content-Type": "application/json"
}


def unique_awbs(awbs):
    seen = set()
    unique = []
    for awb in awbs:
        if awb not in seen:
            seen.add(awb)
            unique.append(awb)
    return unique


def delete_tracking(awb):
    payload = [{"awb": awb, "shipmentStatus": shipment_status}]
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
    except requests.exceptions.RequestException as exc:
        print(f"⚠️ {awb} | Network error | {exc}")
        return

    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text

    if response.ok:
        print(f"✅ {awb} | {response.status_code} | {response_body}")
    else:
        print(f"❌ {awb} | {response.status_code} | {response_body}")


for awb in unique_awbs(awb_list):
    delete_tracking(awb)
    time.sleep(0.3)
