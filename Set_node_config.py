import requests
import json
import time

node_ids = [
388
 
]
CONFIG_VALUE = True
CONFIG_FIELD = "isPodVerificationEnabled"

# base_url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/get_update_node"
base_url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/node/create"
NODE_API_URL = base_url

def fetch_node_data(node_id):
    headers = {
        "node_ids": str(node_id),
        "node_id": str(node_id)
    }
    response = requests.get(NODE_API_URL, headers=headers)
    if response.status_code == 200:
        print("Node data fetched successfully.")
        return response.json()['data']
    else:
        print(f"Error fetching node data: {response.status_code}, {response.text}")
        return None

print(node_ids)


failed_ids = []

for node_id in node_ids:
	
	node_data = fetch_node_data(node_id)
	if node_data is None:
		print(f"ERROR FETCHING NODE DATA FOR NODE ID: {node_id}")
		failed_ids.append(node_id)
		continue

	config_list = json.loads(node_data["nodeConfig"])
	config_list[0][CONFIG_FIELD] = CONFIG_VALUE
	if "active" in node_data:
		del node_data["active"]
	node_data["nodeConfig"] = json.dumps(config_list)
      

	headers = {"Content-Type": "application/json", "node_id": str(node_id)}
	response = requests.put(NODE_API_URL, headers=headers, json=node_data)
	print(f"Node config updated, Status: {response.status_code}")

	if response.status_code != 200:
		print(f"ERROR UPDATING NODE CONFIG FOR NODE ID: {node_id}")
		failed_ids.append(node_id)
		continue

	time.sleep(0.001)
