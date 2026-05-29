import requests

url = 'http://grow-simplee-nlb-prod-a264c46571856f67.elb.ap-south-1.amazonaws.com:9001/awb/sort_to_bin'

headers = {
    'node_id': '1',
    'name': 'saurabh',
    'user_name': 'saurabh',
    'Content-Type': 'application/json'
}

data = {
    "awb": "GS4889621907",
    "status": "info_scan"
}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
