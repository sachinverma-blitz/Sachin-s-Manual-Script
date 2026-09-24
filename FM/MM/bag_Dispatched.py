import pandas as pd
import requests
import time

# ==============================
# CONFIG
# ==============================

FILE_PATH = "query_result_2026-09-24T06_56_40.488695918Z.xlsx"

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/FM_MM/Bag_movements"

# ==============================
# READ EXCEL
# ==============================

df = pd.read_excel(FILE_PATH)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Check required columns
required_columns = ["Bag Number", "Sending Node ID"]

for column in required_columns:
    if column not in df.columns:
        raise Exception(
            f"Missing column: {column}\n"
            f"Available columns: {list(df.columns)}"
        )

print(f"Total bags found: {len(df)}")
print("=" * 60)

success = 0
failed = 0

# ==============================
# PROCESS EACH BAG
# ==============================

for index, row in df.iterrows():

    bag_id = str(row["Bag Number"]).strip()
    node_id = str(row["Sending Node ID"]).strip()

    # Handle Excel numbers like 83.0
    if node_id.endswith(".0"):
        node_id = node_id[:-2]

    if bag_id.endswith(".0"):
        bag_id = bag_id[:-2]

    if not bag_id or bag_id == "nan":
        print(f"⚠️ Row {index + 2}: Bag Number missing")
        failed += 1
        continue

    if not node_id or node_id == "nan":
        print(f"⚠️ Row {index + 2}: Sending Node ID missing for {bag_id}")
        failed += 1
        continue

    headers = {
        "node_id": node_id,
        "name": "Admin",
        "Content-Type": "application/json"
    }

    payload = {
        "bagId": bag_id,
        "type": "DISPATCHED"
    }

    print(
        f"[{index + 1}/{len(df)}] "
        f"Bag: {bag_id} | Sending Node: {node_id}"
    )

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if 200 <= response.status_code < 300:

            print(
                f"    ✅ SUCCESS | "
                f"HTTP {response.status_code} | "
                f"{response.text}"
            )

            success += 1

        else:

            print(
                f"    ❌ FAILED | "
                f"HTTP {response.status_code} | "
                f"{response.text}"
            )

            failed += 1

    except requests.exceptions.RequestException as e:

        print(f"    ❌ ERROR | {e}")
        failed += 1

    # Small gap between API calls
    time.sleep(0.2)


# ==============================
# SUMMARY
# ==============================

print("\n")
print("=" * 60)
print("COMPLETED")
print("=" * 60)

print(f"Total   : {len(df)}")
print(f"Success : {success}")
print(f"Failed  : {failed}")