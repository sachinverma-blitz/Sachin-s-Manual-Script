import pandas as pd
import requests
import time

# Load Excel file
file_path = "query_result_2026-06-16T02_27_22.246790866Z.xlsx"
df = pd.read_excel(file_path)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

print("Detected Columns:", df.columns)

# API URL
url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Trip_complete"

# Static payload
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

# Column mapping
TRIP_COL = "trip id"
RIDER_COL = "tour → rider id"
NAME_COL = "rider → rider name"
POD_COL = "pod"   # <-- pod column

# Loop through rows
for index, row in df.iterrows():
    try:
        headers = {
            "rider_id": str(row[RIDER_COL]),
            "name": str(row[NAME_COL]),
            "Content-Type": "application/json"
        }

        # Fetch pod URL from excel
        pod_url = str(row[POD_COL]).strip()

        payload = STATIC_PAYLOAD.copy()
        payload["tripId"] = int(row[TRIP_COL])

        # Add pod URL dynamically
        payload["podUrls"] = [pod_url]

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        print(
            f"Row {index} | "
            f"TripId {row[TRIP_COL]} | "
            f"POD: {pod_url} | "
            f"Status: {response.status_code}"
        )

        # Optional response print
        print(response.text)

        time.sleep(0.2)

    except Exception as e:
        print(f"Error at row {index}: {e}")