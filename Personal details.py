import requests

def get_bank_details(application_id):
    url = "http://grow-simplee-nlb-prod-a264c46571856f67.elb.ap-south-1.amazonaws.com:9003/application/identityDetails/"
    params = {
        "applicationId": application_id
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            data = data.get('data', {})
            return data.get('accountNumber'), data.get('ifsc')
        else:
            print(f"❌ Failed for Application ID {application_id} | Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"⚠️ Error while fetching Application ID {application_id}: {e}")
        return None, None


if __name__ == "__main__":
    # Single input
    application_id = input("Enter Application ID: ").strip()
    account, ifsc = get_bank_details(application_id)

    if account and ifsc:
        print(f"✅ Application ID: {application_id}")
        print(f"   Account Number: {account}")
        print(f"   IFSC: {ifsc}")
    else:
        print("⚠️ Bank details not found.")
