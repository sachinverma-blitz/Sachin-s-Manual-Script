import requests
import json
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Manualtripclose"

trip_data = [
    {"tripId": 38021185, "reason": "Customer not answering calls"},
    {"tripId": 38033289, "reason": "Customer not answering calls"},
    {"tripId": 38038423, "reason": "Customer not answering calls"},
    {"tripId": 38002337, "reason": "Wrong PIN Code"},
    {"tripId": 38062173, "reason": "Customer not answering calls"},
    {"tripId": 38036111, "reason": "Customer not answering calls"},
    {"tripId": 38065592, "reason": "Wrong PIN Code"},
    {"tripId": 38066810, "reason": "Wrong PIN Code"},
    {"tripId": 38066809, "reason": "Wrong PIN Code"},
    {"tripId": 38069746, "reason": "Phone number is wrong"},
    {"tripId": 38069772, "reason": "Wrong PIN Code"},
    {"tripId": 38070370, "reason": "Customer not answering calls"},
    {"tripId": 38075724, "reason": "Wrong PIN Code"},
    {"tripId": 38078359, "reason": "Wrong PIN Code"},
    {"tripId": 38039963, "reason": "Customer wants to reschedule for tomorrow"},
    {"tripId": 38081176, "reason": "Customer wants to reschedule for tomorrow"},
    {"tripId": 38086745, "reason": "Wrong PIN Code"},
    {"tripId": 38020636, "reason": "Customer not answering calls"},
    {"tripId": 38066746, "reason": "Wrong PIN Code"},
    {"tripId": 38093650, "reason": "Wrong PIN Code"},
    {"tripId": 38093641, "reason": "Wrong PIN Code"},
    {"tripId": 38095136, "reason": "Customer refused to accept"},
    {"tripId": 38069765, "reason": "Wrong PIN Code"},
    {"tripId": 38086248, "reason": "Wrong PIN Code"},
    {"tripId": 38065623, "reason": "Wrong PIN Code"},
    {"tripId": 38065585, "reason": "Wrong PIN Code"},
]

headers = {
    "Content-Type": "application/json"
}

for item in trip_data:
    payload = {
        "tripId": item["tripId"],
        "riderReason": item["reason"],
        "failedDeliveryReason": item["reason"],
        "currentMedium": "manual",
        "isFake": False
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=15
        )

        print(f"Trip ID: {item['tripId']}")
        print(f"Reason : {item['reason']}")
        print(f"Status : {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 60)

    except Exception as e:
        print(f"Failed for Trip ID {item['tripId']} -> {str(e)}")

    time.sleep(0.5)