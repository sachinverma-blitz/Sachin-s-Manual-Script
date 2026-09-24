import pandas as pd
import requests
import time

GET_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/get_update_node"
PUT_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/get_update_node"

# Excel file
EXCEL_FILE = "node.xlsx"

# Read Excel
df = pd.read_excel(EXCEL_FILE)

for _, row in df.iterrows():

    node_id = int(row["node_id"])

    print("=" * 80)
    print(f"Processing Node: {node_id}")

    try:
        # ------------------------------------------------------------------
        # GET EXISTING NODE
        # ------------------------------------------------------------------
        get_headers = {
            "node_ids": str(node_id),
            "node_id": str(node_id)
        }

        get_response = requests.get(GET_URL, headers=get_headers)

        if get_response.status_code != 200:
            print("❌ GET Failed")
            print(get_response.text)
            continue

        response = get_response.json()

        if "data" not in response:
            print("❌ Invalid GET Response")
            print(response)
            continue

        payload = response["data"]

        # ------------------------------------------------------------------
        # STORE OLD VALUES
        # ------------------------------------------------------------------
        old_contact = payload.get("contactName")
        old_phone = payload.get("contactPhone")
        old_active = payload.get("isActive")

        changes = []

        status = str(row["is_active"]).strip().lower()

        if status == "closed":

            if old_active != False:
                payload["isActive"] = False
                changes.append(
                    f"isActive : {old_active} -> False"
                )

        else:

            new_contact = str(row["contact_name"]).strip()
            new_phone = str(row["contact_phone"]).strip()

            if old_contact != new_contact:
                payload["contactName"] = new_contact
                changes.append(
                    f"contactName : '{old_contact}' -> '{new_contact}'"
                )

            if old_phone != new_phone:
                payload["contactPhone"] = new_phone
                changes.append(
                    f"contactPhone : '{old_phone}' -> '{new_phone}'"
                )

            if old_active != True:
                payload["isActive"] = True
                changes.append(
                    f"isActive : {old_active} -> True"
                )

        # ------------------------------------------------------------------
        # NO CHANGES
        # ------------------------------------------------------------------
        if len(changes) == 0:
            print("ℹ️ No changes required.")
            continue

        # ------------------------------------------------------------------
        # PUT UPDATE
        # ------------------------------------------------------------------
        put_headers = {
            "Content-Type": "application/json",
            "node_id": str(node_id)
        }

        put_response = requests.put(
            PUT_URL,
            headers=put_headers,
            json=payload
        )

        # ------------------------------------------------------------------
        # RESULT
        # ------------------------------------------------------------------
        if put_response.status_code == 200:

            print("✅ Update Successful")

            print("Changes Made:")

            for change in changes:
                print("  •", change)

        else:

            print("❌ Update Failed")
            print("Status Code:", put_response.status_code)
            print("Response:", put_response.text)

            print("Attempted Changes:")

            for change in changes:
                print("  •", change)

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(0.2)

print("\nFinished.")