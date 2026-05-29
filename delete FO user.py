import pandas as pd
import requests

# Constants
URL = 'http://grow-simplee-nlb-prod-a264c46571856f67.elb.ap-south-1.amazonaws.com:8002/auth/admin/'
HEADERS = {
    'pool': 'ap-south-1_2nXMZRCaO',
    'Content-Type': 'application/json'
}
USERNAME = '9674154947'

# Load Excel file
df = pd.read_excel('/Users/sachinverma/Library/Mobile Documents/com~apple~CloudDocs/Documents/Scripts/query_result_2025-11-27T15_30_14.688680447Z.xlsx')

# Clean up column names
df.columns = df.columns.str.strip()
print("Columns found in Excel file:", df.columns.tolist())

# Loop through each orgId and make the request
for org_id in df['orgId']:
    print(f"Sending request for orgId: {org_id}")
    payload = {
        "request_type": "delete_user_account",
        "payload": {
            "username": USERNAME
        }
    }
    headers = HEADERS.copy()
    headers['orgId'] = str(org_id)

    response = requests.post(URL, headers=headers, json=payload)

    # Print or log the response
    print(f"Response for orgId {org_id}: {response.status_code} - {response.text}")