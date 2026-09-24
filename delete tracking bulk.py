import requests
import time

# ============================================================
# AWBs
# Paste one AWB per line
# ============================================================

awb_text = """
GS8977558364
"""

# Convert text into list automatically
awb_list = [
    awb.strip()
    for awb in awb_text.splitlines()
    if awb.strip()
]

# ============================================================
# CONFIGURATION
# ============================================================

shipment_status = "Sort to Bin"

url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/tracking/Delete_tracking"

headers = {
    "token": "delete-token-1290",
    "Content-Type": "application/json"
}

# ============================================================
# REMOVE DUPLICATES
# ============================================================

def unique_awbs(awbs):
    return list(dict.fromkeys(awbs))


# ============================================================
# API CALL
# ============================================================

def delete_tracking(awb):
    payload = [
        {
            "awb": awb,
            "shipmentStatus": shipment_status
        }
    ]

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

    except requests.exceptions.RequestException as exc:
        print(f"⚠️ {awb} | Network Error | {exc}")
        return False

    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text

    if response.ok:
        print(
            f"✅ {awb} | "
            f"{response.status_code} | "
            f"{response_body}"
        )
        return True

    else:
        print(
            f"❌ {awb} | "
            f"{response.status_code} | "
            f"{response_body}"
        )
        return False


# ============================================================
# RUN
# ============================================================

unique_list = unique_awbs(awb_list)

print("=" * 60)
print(f"Total AWBs received : {len(awb_list)}")
print(f"Unique AWBs         : {len(unique_list)}")
print(f"Status              : {shipment_status}")
print("=" * 60)

success_count = 0
failed_count = 0

for index, awb in enumerate(unique_list, start=1):

    print(
        f"\n[{index}/{len(unique_list)}] Processing {awb}..."
    )

    success = delete_tracking(awb)

    if success:
        success_count += 1
    else:
        failed_count += 1

    time.sleep(0.001)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PROCESS COMPLETED")
print("=" * 60)
print(f"✅ Successful : {success_count}")
print(f"❌ Failed     : {failed_count}")
print(f"📦 Total      : {len(unique_list)}")
print("=" * 60)