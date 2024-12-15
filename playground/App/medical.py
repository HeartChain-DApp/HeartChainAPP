from web3 import Web3
from listingfollowing import fetch_patients_following_doctor

def show_medical_records():
    doctor_index = 0
    patients = fetch_patients_following_doctor(doctor_index)

    METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Replace with your provider
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    if not web3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum provider.")

    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"  # Replace with your contract address
    contract_abi = [
        {
            "inputs": [
                {"internalType": "address", "name": "patientAddress", "type": "address"}
            ],
            "name": "viewMedicalRecord",
            "outputs": [
                {"internalType": "string[]", "name": "", "type": "string[]"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    patients_with_records = []  # List to store patient info along with their medical records

    if not patients:
        print("No patients found for the given doctor.")
        return patients_with_records  # Return empty list if no patients found
    else:
        for patient in patients:
            patient_address = patient['patient_address']
            try:
                # Fetch the medical records from the contract
                medical_records = contract.functions.viewMedicalRecord(patient_address).call()
                
                # If no medical records, store a message for that patient
                if not medical_records:
                    patients_with_records.append({
                        'first_name': patient['first_name'],
                        'last_name': patient['last_name'],
                        'medical_records': ["No medical records found."]
                    })
                else:
                    # Otherwise, store the patient's medical records
                    patients_with_records.append({
                        'first_name': patient['first_name'],
                        'last_name': patient['last_name'],
                        'medical_records': medical_records
                    })

            except Exception as e:
                print(f"Error fetching medical record for {patient['first_name']} {patient['last_name']}: {e}")
                patients_with_records.append({
                    'first_name': patient['first_name'],
                    'last_name': patient['last_name'],
                    'medical_records': ["Error fetching records."]
                })

    return patients_with_records  # Return the list of patients with medical records
