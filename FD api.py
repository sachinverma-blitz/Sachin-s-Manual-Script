import requests
import json
from datetime import datetime
import time
import warnings

warnings.filterwarnings("ignore")

# ✅ SAME AS CURL
API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/tracking/Update_shipment_status"
HEADERS = {"Content-Type": "application/json"}

# 🔹 BULK DATA
awb_user_pairs =[
  {"awb": "NBG764306728", "userId": 554}
]
def send_update(awb, user_id):
    payload = [
        {
            "awb": awb,
            "location": "Bangalore",
            "userId": user_id,
            "shipperId": 301,
            "updateTime": datetime.now().strftime("%m/%d/%Y %H:%M"),
            "remark": "Customer wants to reschedule for tomorrow",
            "shipmentStatus": "Failed Delivered"
        }
    ]

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,   # ✅ better than data=json.dumps
            timeout=20
        )

        if response.status_code == 200:
            print(f"✅ Success → {awb}")
        else:
            print(f"❌ Failed → {awb} | {response.status_code} | {response.text}")

    except Exception as e:
        print(f"⚠ Error → {awb} | {str(e)}")


# 🔹 LOOP
for item in awb_user_pairs:
    send_update(item["awb"], item["userId"])
    time.sleep(0.3)
