import requests
import time

# API URL
BASE_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/Rider_Attendance"

# Rider IDs (cleaned list)
rider_ids = [
31291,29704,29708,24724,25964,28239,25958,26180,26170



]

# Loop through each rider_id
for rider_id in rider_ids:
    try:
        url = f"{BASE_URL}?rider_ids={rider_id}"
        
        response = requests.post(url)

        print(f"Rider ID: {rider_id} | Status: {response.status_code} | Response: {response.text}")

        # Optional delay to avoid rate limit
        time.sleep(0.3)

    except Exception as e:
        print(f"Error for Rider ID {rider_id}: {e}")