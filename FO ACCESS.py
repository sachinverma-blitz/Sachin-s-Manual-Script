import requests
import json

# ------------------------------
# Configuration
# ------------------------------

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"
POOL = "ap-south-1_2nXMZRCaO"
PHONE = "+917439315913"        # From curl
GROUP_IDS = ["City Head"]      # From curl

JSON_FILE = "kanhaiya_orgs.json"


# ------------------------------
# Load JSON Records
# ------------------------------

with open(JSON_FILE, "r") as f:
    records = json.load(f)

print(f"Loaded {len(records)} records.\n")


# ------------------------------
# Send Requests in Loop
# ------------------------------

for rec in records:
    org_id = rec["orgId"]
    alias = rec["alias"]
    name = rec["name"]

    payload = {
        "request_type": "add_user",
        "payload": {
            "phone": PHONE,
            "is_mfa_required": False,
            "group_ids": GROUP_IDS,
            "alias": alias,
            "metadata": {
                "name": name
            }
        }
    }

    headers = {
        "pool": POOL,
        "orgId": str(org_id),
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)

        print(f"➡️ OrgID: {org_id}, Alias: {alias}")
        print("Status:", response.status_code)

        try:
            print("Response:", response.json())
        except:
            print("Response Text:", response.text)

    except Exception as e:
        print(f"❌ Error for OrgID {org_id}:", str(e))

    print("--------------------------------------------------")