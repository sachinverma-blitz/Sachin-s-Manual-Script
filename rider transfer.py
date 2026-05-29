import requests

url = "https://35idc7phd7.execute-api.ap-south-1.amazonaws.com/V1/sarathyupdate/ridertransfer"

headers = {
    "node_id": "125",
    "name": "sachin",
    "Content-Type": "application/json"
}

# Your bulk rider IDs
rider_ids = [
    16638,19015,19106,19724,23701,20202,10512,22187,25349,23187,22420,25182,24109,24113,24508,25124,25681,17969,15631,17968,23475,25864
    ]

payload = {
    "nodeId": 125,
    "riderIds": rider_ids
}

response = requests.put(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text)