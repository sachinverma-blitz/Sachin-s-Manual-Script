import requests
import time

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/finops/manual-deposit"

data = [
  {"orgId": "51", "amount": 225400, "ref": "fnf settlement for SDEX-Franchise node 51 on 13-05-2026"},
  {"orgId": "243", "amount": 95000, "ref": "fnf settlement for CKPT-Franchise node 243 on 13-05-2026"},
  {"orgId": "221", "amount": 164617.54, "ref": "fnf settlement for NOJP-Franchise node 221 on 13-05-2026"},
  {"orgId": "73", "amount": 93080, "ref": "fnf settlement for BANR-Franchise node 73 on 13-05-2026"},
  {"orgId": "299", "amount": 139802, "ref": "fnf settlement for MERT-Franchise node 299 on 13-05-2026"},
  {"orgId": "110", "amount": 162632, "ref": "fnf settlement for LKMH-Franchise node 110 on 13-05-2026"}
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

    time.sleep(0.5)
