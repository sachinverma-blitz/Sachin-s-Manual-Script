import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/FM_MM/Bag_movements"

HEADERS = {
    "node_id": "309",
    "name": "Admin",
    "Content-Type": "application/json"
}

# Add your Bag IDs here
BAG_IDS = [




383749830001,
602452262636,
882566804406,
338559334827,
824594319764,
521127010307,
524729351465,
124310381145,
607274078792,
329432775300,
165287880628,
971821449158]

for bag_id in BAG_IDS:

    payload = {
        "bagId": bag_id,
        "type": "RECEIVED"
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        print(f"Bag ID: {bag_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 60)

    except requests.exceptions.RequestException as e:
        print(f"Bag ID: {bag_id}")
        print(f"ERROR: {e}")
        print("-" * 60)

    # Small delay between requests
    time.sleep(0.2)