import pandas as pd
import requests

FILE_PATH = "query_result_2026-03-27T15_40_22.756705942Z.xlsx"

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Trip_complete"


def load_excel(file_path):
    df = pd.read_excel(file_path)

    # clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    print("✅ Columns detected:", df.columns.tolist())
    return df


def complete_trip(row):
    try:
        rider_id = row.get("rider_→_rider_id")
        name = row.get("rider_→_rider_name")
        trip_id = row.get("trip_id")
        lat = row.get("location_→_lat")
        lng = row.get("location_→_lng")

        # fallback if odometer not present
        odometer = row.get("distance", 0)

        # 🚨 validation
        if pd.isna(rider_id) or pd.isna(name) or pd.isna(trip_id):
            print("⚠️ Missing critical data, skipping row")
            return "SKIPPED"

        headers = {
            "rider_id": str(int(rider_id)),
            "name": str(name),
            "Content-Type": "application/json"
        }

        payload = {
            "tripId": int(trip_id),
            "deliveredTo": "store",
            "remarks": "",
            "podUrls": [""],
            "isOtpVerified": True,
            "actionLat": float(lat) if not pd.isna(lat) else 0,
            "actionLng": float(lng) if not pd.isna(lng) else 0,
            "odometer": int(odometer) if not pd.isna(odometer) else 0,
            "isRiderVerified": True,
            "locationType": "office"
        }

        response = requests.post(URL, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            print(f"✅ Trip {trip_id} SUCCESS")
            return "SUCCESS"
        else:
            print(f"❌ Trip {trip_id} FAILED:", response.text)
            return "FAILED"

    except Exception as e:
        print(f"🚨 Error:", str(e))
        return "ERROR"


def main():
    df = load_excel(FILE_PATH)

    results = []

    for i, row in df.iterrows():
        print(f"\n🔄 Processing row {i+1}")
        result = complete_trip(row)
        results.append(result)

    df["status"] = results
    df.to_excel("output_results.xlsx", index=False)

    print("\n📁 Results saved to output_results.xlsx")


if __name__ == "__main__":
    main()