import pandas as pd
import requests
import time

# File path — update to the Excel export containing the rows to deactivate
EXCEL_PATH = "rider_bookings.xlsx"

# APIs
BOOKING_API_URL = "https://fcss60g2yf.execute-api.ap-south-1.amazonaws.com/v1/mg-rider-booking"
ZONES_API_URL = "https://fcss60g2yf.execute-api.ap-south-1.amazonaws.com/v1/zone-polygons"

# Column Mapping
RIDER_ID_COL = "Rider ID"
START_TIME_COL = "Start Time"
END_TIME_COL = "End Time"
LAT_COL = "Latitude"
LNG_COL = "Longitude"
AREA_NAME_COL = "Area Name"
AMOUNT_COL = "Amount"

# Read Excel
df = pd.read_excel(EXCEL_PATH)

# Fetch zone polygons once (Zone Name -> Polygon)
zones_response = requests.post(
    ZONES_API_URL,
    headers={"Content-Type": "application/json", "username": "abc"},
    json={"type": "get_all_ondemand_polygons"}
)
zone_map = {
    z["zone_name"]: z.get("polygon_json")
    for z in zones_response.json().get("data", [])
    if z.get("zone_name")
}

for index, row in df.iterrows():
    try:
        rider_id = int(row[RIDER_ID_COL])
        start_ts = int(pd.to_datetime(row[START_TIME_COL]).timestamp())
        end_ts = int(pd.to_datetime(row[END_TIME_COL]).timestamp())
        lat = float(row[LAT_COL])
        lng = float(row[LNG_COL])
        name = row[AREA_NAME_COL]
        amount = int(row[AMOUNT_COL])
        polygon = zone_map.get(name)

        payload = {
            "rider_id": rider_id,
            "start_time": start_ts,
            "end_time": end_ts,
            "lat": lat,
            "lng": lng,
            "is_active": False,
            "name": name,
            "amount": amount,
            "polygon": polygon
        }

        response = requests.post(BOOKING_API_URL, json=payload)
        print(f"[{index+1}] Rider {rider_id} | Status: {response.status_code} | {response.text}")

    except Exception as e:
        print(f"[{index+1}] Error: {e}")

    time.sleep(0.4)

print("✅ Done.")
