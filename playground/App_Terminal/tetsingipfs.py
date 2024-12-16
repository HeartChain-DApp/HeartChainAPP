import requests
import json

# Define the URL of your IPFS node's HTTP API (make sure IPFS daemon is running)
ipfs_api_url = 'http://127.0.0.1:5001/api/v0/'

# Function to upload data to IPFS
def upload_to_ipfs(data):
    try:
        # The IPFS API endpoint for adding a JSON file
        url = ipfs_api_url + 'add'
        
        # Make a POST request to add the data to IPFS
        response = requests.post(url, files={'file': ('data.json', json.dumps(data), 'application/json')})

        # Check if the upload was successful
        if response.status_code == 200:
            ipfs_hash = response.json().get('Hash')
            print(f"Data uploaded to IPFS with hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading data to IPFS: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Example data to upload
data = {
    "patientAddress": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
    "diagnostic": "Fever",
    "nurseName": "Nurse Jane",
    "roomNumber": "Room 101",
    "timeOfVisit": 1632345600
}

# Upload data to IPFS
upload_to_ipfs(data)
