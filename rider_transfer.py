import requests
import time

url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/ridertransfer"

headers = {
    "node_id": "125",
    "name": "sachin",
    "Content-Type": "application/json"
}

# Add all rider IDs here
rider_ids = [
  26583,25884,25801,25786,25781,25707,25700,25530,25529,25511,25500,25476,25430,25359,25324,25316,25287,25245,25149,25117,25106,25022,24923,24672,24575,24200,22702,22618,22616,22606,22605,22604,22600,22598,22596,22587,22580,22579,22577,22574,22571,22556,22552,22550,22548,22543,22541,22537,22526,22524,22515,22513,22504,22497,22494,22493,22489,22484,22467,22465,22290,22046

]

for rider_id in rider_ids:
    payload = {
        "nodeId": 125,
        "riderIds": [rider_id]
    }

    try:
        response = requests.put(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"Rider ID: {rider_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 50)

        # Pause 2 seconds before next request
        time.sleep(2)

    except Exception as e:
        print(f"Failed for Rider ID {rider_id}: {e}")
        time.sleep(5)