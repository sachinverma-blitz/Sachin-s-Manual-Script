import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/bag_movement/in_scan"

HEADERS = {
    "node_id": "249",
    "name": "tech",
    "Content-Type": "application/json"
}

BAG_IDS =[

570724382521,    
448350592532,    
934471338674,    
931613636630,    
151863790541,    
144352052269,    
427193088001,    
349586547980,    
358493193083,    
840744161984,    
799432657771,    
660252470367,    
184315540804,    
678734695327,    
593106381051,    
386866979350,    
438130060430,    
766188989655,    
280982263173,    
268868437840,    
775294443834,    
429919651763,    
940827331348,    
128224391881,    
781125489860






]
def in_scan_bags():
    success_count = 0
    failed_count = 0

    for bag_id in BAG_IDS:
        payload = {
            "bagId": bag_id,
            "type": "RECEIVED"
        }

        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=30
            )

            if response.ok:
                success_count += 1
                print(f"✅ {bag_id}: SUCCESS | {response.text}")
            else:
                failed_count += 1
                print(
                    f"❌ {bag_id}: FAILED | "
                    f"HTTP {response.status_code} | {response.text}"
                )

        except requests.RequestException as error:
            failed_count += 1
            print(f"❌ {bag_id}: ERROR | {error}")

        # Small delay between requests
        time.sleep(0.5)

    print("\n========== SUMMARY ==========")
    print(f"Total bags : {len(BAG_IDS)}")
    print(f"Successful : {success_count}")
    print(f"Failed     : {failed_count}")


if __name__ == "__main__":
    confirmation = input(
        f"This will in-scan {len(BAG_IDS)} bags at Node 6. Continue? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        in_scan_bags()
    else:
        print("Operation cancelled.")