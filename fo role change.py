import requests

url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

org_ids = [

  "313",
  "149",
  "98",
  "196",
  "99",
  "96",
  "125",
  "202",
  "312",
  "195",
  "167",
  "161",
  "203"

]

for org_id in org_ids:
    headers = {
        "pool": "ap-south-1_2nXMZRCaO",
        "orgId": org_id,
        "username": "Hemanth",
        "Content-Type": "application/json"
    }

    payload = {
        "request_type": "change_user_permission",
        "payload": {
            "username": "7892325692",
            "group_ids": ["Quick Team Lead"],
            "type": "REPLACE"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print(f"OrgId: {org_id}, Status: {response.status_code}")