
import pandas as pd
import requests
import time

# =========================
# CONFIGURATION
# =========================
EXCEL_FILE = "query_result_2026-08-06T09_48_01.690265546Z.xlsx"
API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

# User Details (same for all rows)
PHONE = "+916362485920"
NAME = "Devansh"
GROUP_IDS = ["City Head"]
IS_MFA_REQUIRED = False

HEADERS = {
    "pool": "ap-south-1_2nXMZRCaO",
    "Content-Type": "application/json"
}

# =========================
# READ EXCEL
# =========================
df = pd.read_excel(EXCEL_FILE, dtype=str)

# =========================
# API HIT LOOP
# =========================
for index, row in df.iterrows():
    org_id = str(row["orgId"]).strip()
    alias = str(row["alias"]).strip()

    headers = {
        **HEADERS,
        "orgId": org_id
    }

    payload = {
        "request_type": "add_user",
        "payload": {
            "phone": PHONE,
            "is_mfa_required": IS_MFA_REQUIRED,
            "group_ids": GROUP_IDS,
            "alias": alias,
            "metadata": {
                "name": NAME
            }
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=15
        )

        print(f"[{index + 1}] OrgID: {org_id} | Alias: {alias}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 80)

    except Exception as e:
        print(f"Error for OrgID {org_id} | Alias {alias}: {e}")

    # Small delay to avoid throttling
    time.sleep(0.0001)

print("Bulk process completed.")
