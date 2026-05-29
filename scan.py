import requests

# ==== CONFIGURATION ====
API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Index_order_scan"
HEADERS = {
    "Content-Type": "application/json",
    "orgId": "1"
}

# ==== INPUT: List of suborder IDs ====
suborder_ids = [


42564170

]
# ==== REQUEST PAYLOAD ====
payload = {
    "orderIds": [],
    "suborderIds": suborder_ids
}

# ==== SEND PATCH REQUEST ====
try:
    response = requests.patch(API_URL, json=payload, headers=HEADERS)
    
    # Print status and response
    print(f"Status Code: {response.status_code}")
    if response.content:
        print("Response Body:", response.json())
    else:
        print("No content returned.")
except Exception as e:
    print(f"Error during request: {e}")
