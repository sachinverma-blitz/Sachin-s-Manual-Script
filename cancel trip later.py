import requests

# List of trip IDs to cancel
trip_ids = [




51587615,
51587238,
51587260,
51587661,
51587254,
51587601,
51587694,
51587578,
51587667,
51586832,
51587240,
51587241,
51587239,
51587257,
51587242,
51587243,
51587244,
51587245,
51587246,
51587247,
51587248,
51587249,
51587250,
51587251,
51587252,
51587253,
51587255,
51587256,
51587258,
51587259,
51587562,
51587595,
51587677,
51587697]


url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Manualtripclose"

headers = {
    "Content-Type": "application/json"
}

for trip_id in trip_ids:
    payload = {
        "tripId": trip_id,
        "riderReason": "Customer wants to reschedule for later today",
        "failedDeliveryReason": "Customer wants to reschedule for later today",
        "currentMedium": "manual",
        "isFake": False
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.ok:
        print(f"Successfully cancelled trip {trip_id}: {response.json()}")
    else:
        print(f"Failed to cancel trip {trip_id}: {response.status_code} - {response.text}")
