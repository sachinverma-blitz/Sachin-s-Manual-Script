import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

POOL_ID = "ap-south-1_2nXMZRCaO"
USERNAME = "6362485920"

ORG_IDS =[
   7, 366, 129, 116, 222, 117, 49, 6, 104, 3, 70, 362, 121, 249, 287, 339,
    223, 5, 94, 39, 234, 224, 135, 59, 69, 154, 237, 252, 380, 193, 172, 29,
    73, 1, 289, 369, 43, 188, 19, 351, 357, 64, 209, 61, 26, 134, 93, 242,
    372, 36, 68, 192, 130, 336, 301, 220, 187, 364, 356, 349, 338, 354, 146,
    148, 334, 27, 378, 376, 199, 228, 248, 328, 45, 355, 365, 54, 373, 105,
    310, 75, 189, 241, 102, 236, 74, 245, 243, 353, 368, 225, 381, 51, 348,
    80, 299, 306, 2, 308, 227, 155, 293, 221, 230, 218, 124, 231, 318, 185,
    344, 374, 343, 377, 371, 350, 291, 163, 319, 370, 294, 84, 352, 204, 302,
    56, 346, 171, 145, 296, 41, 297, 367, 207, 214, 360, 363, 87, 359, 285,
    158, 106, 90, 290, 295, 110, 219, 165, 345, 40, 205, 83, 326, 22, 86, 23,
    24, 251, 300, 162, 247, 298, 139, 309, 375, 246, 337, 21, 200, 358, 340,
    79, 256, 250, 197, 229, 361, 179, 89, 347, 327
]



for i, org_id in enumerate(ORG_IDS, start=1):
    headers = {
        "pool": POOL_ID,
        "orgId": str(org_id),
        "Content-Type": "application/json"
    }

    payload = {
        "request_type": "delete_user_account",
        "payload": {
            "username": USERNAME
        }
    }

    r = requests.post(API_URL, headers=headers, json=payload)

    if r.status_code == 200:
        print(f"✅ {i}. Deleted {USERNAME} | Org {org_id}")
    else:
        print(f"❌ {i}. Failed | Org {org_id} | {r.text}")

    time.sleep(0.0001)
