import requests
import pandas as pd

def get_bank_details(application_id):
    url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/RIder_bankdetails"
    params = {"applicationId": application_id}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get('data', {})
        return {
            'applicationId': application_id,
            'fullName' : data.get ('fullName'),
            'accountNumber': data.get('accountNumber'),
            'ifsc': data.get('ifsc'),
            'dlNumber' : data.get('dlNumber'),
            'ExistingEntityID' : data.get('ExistingEntityID'),
            'error': None
        }
    except Exception as e:
        return {
            'applicationId': application_id,
            'fullName' : None,
            'accountNumber': None,
            'ifsc': None,
            'dlNumber': None,
            'ExistingEntityID' : None,
            'error': str(e)
        }

# ✅ Application IDs
application_ids =[
57237,70468,70670,70690,54321,70787,71482,70925,70976,70993,71056,71052,71104,71094,71110,71118,71771,71121,72088,65530,71161,71222,71228,71661,71289,68352,72266,72262,71411

]


 # Replace with actual IDs

# Collect all results
results = [get_bank_details(app_id) for app_id in application_ids]

# Convert to DataFrame
df = pd.DataFrame(results)

# Save to Excel (.xlsx format)
df.to_excel('bank_details13.xlsx', index=False)

print("✅ Saved to 'bank_details13.xlsx'")






