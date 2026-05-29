import requests
import json

# List of AWBs to update
awb_list = [
   "GS8930682122"
]

    # Add more AWBs here


# Single status for all
shipment_status = ("Failed Delivered")  # Change to desired status (e.g., "Failed Delivered", "Picked-up", etc.)

# Create payload: one object per AWB with the same status
payload = [{"awb": awb, "shipmentStatus": shipment_status} for awb in awb_list]

# API endpoint
url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/tracking/Delete_tracking"

# Headers
headers = {
    "token": "delete-token-1290",
    "Content-Type": "application/json"
}

# Send request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print response
print(f"Status Code: {response.status_code}")
try:
    print(response.json())
except Exception:
    print(response.text)
