import requests

def delete_tour(tour_id):
    base_url = "http://growsimplee-nlb-93f0a1d7f78cb8d6.elb.ap-south-1.amazonaws.com:9001/tour/create"
    params = {"tourId": tour_id}

    try:
        response = requests.delete(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (4XX or 5XX)
        
        # Print response details
        print(f"✅ DELETE request successful for tourId: {tour_id}")
        print(f"Status Code: {response.status_code}")
        if response.text:
            print("Response Content:")
            print(response.text)
        else:
            print("No content returned.")
        
        return response.json() if response.text else None

    except requests.RequestException as e:
        print(f"❌ Error deleting tourId {tour_id}: {e}")
        return None

# Example usage
tour_id = [
3156247,
3156253,
3156243,
3156253,
3156243,
3156249 ] # Or replace with a variable/list for bulk
result = delete_tour(tour_id)
