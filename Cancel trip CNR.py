import requests

# API endpoint
url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Manualtripclose"

# Headers
headers = {
    "Content-Type": "application/json"
}

# List of trip IDs (paste your bulk IDs here)
trip_ids = [

43555559

    # ... add more here
]

# Loop through and cancel each trip
for trip_id in trip_ids:
    payload = {
        "tripId": trip_id,
        "riderReason": "Customer not answering calls",
        "failedDeliveryReason": "Customer not answering calls",
        "currentMedium": "manual",
        "isFake": False
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"✅Trip ID: {trip_id} -> Status: {response.status_code}, Response: {response.text}")
