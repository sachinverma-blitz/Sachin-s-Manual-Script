import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# =====================
# CONFIGURATION
# =====================

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/RIder_bankdetails"

MAX_WORKERS = 20  # increase to 30 if needed


# =====================
# SESSION SETUP (FASTER)
# =====================

session = requests.Session()


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

application_ids =[
   

113750,
113735,
113695,
113632,
113653,
113633,
113214,
113321,
113282,
113256,
112958,
113231,
112990,
112960,
112903,
112872,
112828,
112686,
112649,
112594,
112376,
112253,
111963,
112111,
112090,
111767,
111753,
111759,
111677,
111653,
111529,
111446,
111069,
110990,
110769,
110414,
110525,
110372,
110028,
109993,
109895,
109735,
109731,
109481,
109447,
109394,
109357,
108846,
109360,
108814,
109048,
108997,
108855,
108829,
108771,
108470,
108140,
108018,
107361,
107302,
107023,
106847,
106760,
106607,
106491,
106543,
106048,
105979,
105884,
105620,
105509,
105494,
105226,
104906,
105126,
104516,
104514,
104334,
104184,
104061,
104106,
102266,
102434,
101905,
101269,
101020,
100669,
100272,
100195,
99820,
99628,
99226,
98983,
98838,
98529,
98395,
97880,
96317,
95840,
95820,
95573,
95264,
94393,
93884,
92229,
90829,
90548,
89509,
88246,
87965,
85399,
80491,
80033,
79733,
79250,
77073,
76360,
74521,
73325,
73160,
72881,
72844,
70474,
67231,
66308,
63457,
61495,
61465,
60657,
60528,
60190,
58604,
58105,
57788,
57507,
55233,
53111,
51950,
51890,
51817,
51806,
51759,
51714,
51622,
51487,
51217,
50980,
50188,
49954,
49702,
48509,
47510,
47013,
46703,
44110,
41125,
17710

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