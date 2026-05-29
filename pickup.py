import pandas as pd
import requests
import time

# File path
EXCEL_PATH = "Scripts/query_result_2026-05-29T06_40_19.058010237Z.xlsx"

# APIs
PICKUP_API = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Pickup_task"
TRIP_API = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Trip_complete"

# Read Excel
df = pd.read_excel(EXCEL_PATH)

# Column Mapping
TRIP_COL = "Pickup Task Trip ID"
TASK_ENTITY_COL = "Task Entity ID"
RIDER_COL = "Rider → Rider ID"
NAME_COL = "Rider → Rider Name"

# Trip complete static payload
STATIC_PAYLOAD = {
    "deliveredTo": "",
    "remarks": "",
    "podUrls": [""],
    "isOtpVerified": True,
    "actionLat": 12.931941,
    "actionLng": 77.622396,
    "odometer": 2100,
    "isRiderVerified": True,
    "locationType": "office"
}

for index, row in df.iterrows():
    try:
        trip_id = int(row[TRIP_COL])
        task_entity_id = int(row[TASK_ENTITY_COL])
        rider_id = str(row[RIDER_COL])
        rider_name = str(row[NAME_COL])

        # ----------- STEP 1: Pickup Task Complete -----------
        pickup_payload = {
            "tripId": trip_id,
            "taskEntityId": task_entity_id,
            "status": "COMPLETED",
            "reason": "",
            "pickupOtp": ""
        }

        pickup_headers = {
            "rider_id": rider_id,
            "Content-Type": "application/json"
        }

        pickup_response = requests.post(PICKUP_API, headers=pickup_headers, json=pickup_payload)

        print(f"[{index+1}] Pickup | Trip {trip_id} | Status: {pickup_response.status_code}")

        # ----------- STEP 2: Trip Complete (Only if success) -----------
        if pickup_response.status_code == 200:
            trip_payload = STATIC_PAYLOAD.copy()
            trip_payload["tripId"] = trip_id

            trip_headers = {
                "rider_id": rider_id,
                "name": rider_name,
                "Content-Type": "application/json"
            }

            trip_response = requests.post(TRIP_API, headers=trip_headers, json=trip_payload)

            print(f"[{index+1}] Trip Complete | Trip {trip_id} | Status: {trip_response.status_code}")

        else:
            print(f"[{index+1}] Skipping Trip Complete due to Pickup failure")

    except Exception as e:
        print(f"[{index+1}] Error: {e}")

    time.sleep(0.5)

print("✅ Full process completed.")