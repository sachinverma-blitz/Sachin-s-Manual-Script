import requests
import time

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/finops/manual-deposit"

data =[
  {"orgId":"145","amount":36550.26,"ref":"Manual Removal for Re: GST payment not recived GOLDEN ICE for GGMS-Franchise"},
  {"orgId":"117","amount":93248.1,"ref":"Manual Removal for Re: GST payment not recived GOLDEN ICE for GGPV-Franchise"}
]
for item in data:
    headers = {
        "orgId": item["orgId"],
        "Content-Type": "application/json"
    }

    payload = {
        "bank_slip_url": [""],
        "amount": item["amount"],
        "ref_id": item["ref"]
    }

    r = requests.post(URL, headers=headers, json=payload)

    print(f'ORG {item["orgId"]} | {item["ref"]} | {r.status_code}')
    print(r.text)
    print("-" * 50)

    time.sleep(0.01)
