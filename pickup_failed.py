import pandas as pd
import requests
import time

# ========= CONFIG =========
FILE_PATH = "Scripts/query_result_2026-05-04T08_11_39.442589556Z.xlsx"

PICKUP_FAIL_API = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Pickup_fail"
TRIP_COMPLETE_API = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Trip_complete"

SLEEP_TIME = 0.2

# ========= LOAD FILE =========
df = pd.read_excel(FILE_PATH)
df.columns = df.columns.str.strip().str.lower()

# ========= COLUMN MAPPING =========
trip_col = "pickup task trip id"
task_col = "task entity id"
node_col = "tour → node id"
rider_col = "rider → rider id"

# ========= COUNTERS =========
fail_success = 0
complete_success = 0
failed = 0

# ========= LOOP =========
for index, row in df.iterrows():
    try:
        trip_id = int(row[trip_col])
        task_id = int(row[task_col])
        node_id = str(int(row[node_col]))
        rider_id = str(int(row[rider_col]))

        # ===== 1. PICKUP FAIL =====
        fail_headers = {
            "node_id": node_id,
            "Content-Type": "application/json"
        }

        fail_payload = {
            "tripId": trip_id,
            "taskEntityId": task_id,
            "status": "FAILED",
            "reason": "Store Delaying Handover",
            "pickupOtp": "",
            "riderId": int(rider_id)
        }

        fail_response = requests.post(PICKUP_FAIL_API, headers=fail_headers, json=fail_payload)

        if fail_response.status_code != 200:
            print(f"❌ Pickup Fail Failed | Trip: {trip_id} | {fail_response.text}")
            failed += 1
            continue

        print(f"✅ Pickup Failed Done | Trip: {trip_id}")
        fail_success += 1

        # ===== 2. TRIP COMPLETE =====
        complete_headers = {
            "rider_id": rider_id,
            "name": "a",
            "Content-Type": "application/json"
        }

        complete_payload = {
            "tripId": trip_id,
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

        complete_response = requests.post(TRIP_COMPLETE_API, headers=complete_headers, json=complete_payload)

        if complete_response.status_code == 200:
            print(f"✅ Trip Completed | Trip: {trip_id}")
            complete_success += 1
        else:
            print(f"❌ Trip Complete Failed | Trip: {trip_id} | {complete_response.text}")
            failed += 1

    except Exception as e:
        print(f"⚠️ Error | Row {index} | {str(e)}")
        failed += 1

    time.sleep(SLEEP_TIME)


# ========= SUMMARY =========
print("\n===== SUMMARY =====")
print(f"✅ Pickup Failed: {fail_success}")
print(f"✅ Trip Completed: {complete_success}")
print(f"❌ Failed: {failed}")