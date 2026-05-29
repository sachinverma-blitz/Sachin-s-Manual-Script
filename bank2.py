import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# =====================
# CONFIGURATION
# =====================

API_URL = "https://35idc7phd7.execute-api.ap-south-1.amazonaws.com/V1/Rider_Details/RIder_identityDetails"

API_KEY = "SYwfFp7Bdg8o25hrja5g8ffiAXzTX5L3KuSRCwu7"

MAX_WORKERS = 20  # increase to 30 if needed


# =====================
# SESSION SETUP (FASTER)
# =====================

session = requests.Session()
session.headers.update({
    "x-api-key": API_KEY
})


# =====================
# FUNCTION TO FETCH DATA
# =====================

def get_bank_details(application_id):

    params = {"applicationId": application_id}

    try:
        response = session.get(
            API_URL,
            params=params,
            timeout=(5, 20)
        )

        response.raise_for_status()

        json_data = response.json()

        data = json_data.get("data", {})

        return {
            "applicationId": application_id,
            "fullName": data.get("fullName"),
            "accountNumber": data.get("accountNumber"),
            "ifsc": data.get("ifsc"),
            "dlNumber": data.get("dlNumber"),
            "ExistingentityID": data.get("ExistingentityID"),
            "error": None
        }

    except Exception as e:

        return {
            "applicationId": application_id,
            "fullName": None,
            "accountNumber": None,
            "ifsc": None,
            "dlNumber": None,
            "ExistingentityID": None,
            "error": str(e)
        }


# =====================
# APPLICATION IDs
# =====================

application_ids = [
  10721,
  12212,
  2468,
  48929,
  10323,
  48606,
  48432,
  43814,
  45750,
  49182,
  49447,
  49757,
  49901,
  49972,
  49961,
  49880,
  49977,
  50001,
  11356,
  50265,
  50072,
  51143,
  51490,
  49946,
  47243,
  13843
]


# =====================
# BULK EXECUTION
# =====================

results = []
completed = 0
total = len(application_ids)

print(f"Starting bulk fetch for {total} IDs...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = {
        executor.submit(get_bank_details, app_id): app_id
        for app_id in application_ids
    }

    for future in as_completed(futures):

        result = future.result()
        results.append(result)

        completed += 1

        print(f"Completed {completed}/{total}")


# =====================
# FINAL SAVE
# =====================

df = pd.DataFrame(results)

df.to_excel("bank_details_final.xlsx", index=False)

print("✅ Completed successfully")
print("Saved as bank_details_final.xlsx")
