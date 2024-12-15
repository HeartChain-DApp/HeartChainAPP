import json
from web3 import Web3

def fetch_and_save_patient_data():
    # Define the provider URL for MetaMask (or your local Ethereum node)
    METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Replace with your provider
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    # Ensure the connection is successful
    if not web3.is_connected():
        print("Failed to connect to the provider.")
        return

    print("Connected to the Ethereum provider.")

    # Contract ABI and address (replace with actual values)
    contract_address = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"  # Replace with your contract address
    contract_abi = [
        {
            "inputs": [],
            "name": "viewAllPatients",
            "outputs": [
                {
                    "internalType": "address[]",
                    "name": "",
                    "type": "address[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "name": "patients",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "firstName",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "lastName",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "birthDate",
                    "type": "uint256"
                },
                {
                    "internalType": "string",
                    "name": "addressDetails",
                    "type": "string"
                },
                {
                    "internalType": "address",
                    "name": "patientAddress",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    # Initialize contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Call the viewAllPatients function to get patient addresses
    def fetch_patients():
        try:
            patients = contract.functions.viewAllPatients().call()
            return patients
        except Exception as e:
            print(f"Error fetching patients: {e}")
            return []

    # Call the patients function to get details of a specific patient
    def fetch_patient_details(patient_address):
        try:
            patient_details = contract.functions.patients(patient_address).call()
            return patient_details
        except Exception as e:
            print(f"Error fetching details for patient {patient_address}: {e}")
            return None

    # Fetch all patients
    patients = fetch_patients()

    # Store patient details in a dictionary
    patient_data = []

    if patients:
        print(f"List of patients: {patients}")
        # For each patient, fetch and store their details
        for patient_address in patients:
            details = fetch_patient_details(patient_address)
            if details:
                first_name, last_name, birth_date, address_details, patient_address = details
                patient_info = {
                    "Patient Address": patient_address,
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Birth Date": birth_date,
                    "Address Details": address_details
                }
                patient_data.append(patient_info)
    else:
        print("No patients found.")

    # Save the patient data to a JSON file
    if patient_data:
        with open("patients_data.json", "w") as json_file:
            json.dump(patient_data, json_file, indent=4)
        print("Patient data saved to patients_data.json.")
    else:
        print("No patient data to save.")

# Call the function to fetch and save patient data
fetch_and_save_patient_data()
