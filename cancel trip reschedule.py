import requests

# List of trip IDs to cancel
trip_ids = [



37905865
]


url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Manualtripclose"

headers = {
    "Content-Type": "application/json"
}

for trip_id in trip_ids:
    payload = {
        "tripId": trip_id,
        "riderReason": "Customer wants to reschedule for tomorrow",
        "failedDeliveryReason": "Customer wants to reschedule for tomorrow",
        "currentMedium": "manual",
        "isFake": False
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.ok:
        print(f"✅Successfully cancelled trip {trip_id}: {response.json()}")
    else:
        print(f"❌Failed to cancel trip {trip_id}: {response.status_code} - {response.text}")
