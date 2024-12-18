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

    if not patients:
        print("No patients found for the given doctor.")
    else:
        for patient in patients:
            patient_address = patient['patient_address']
            try:
                medical_records = contract.functions.viewMedicalRecord(patient_address).call()
                
                if not medical_records:
                    print(f"No medical records found for {patient['first_name']} {patient['last_name']}.")
                else:
                    

                    for record in medical_records:
                        print(f" - {record}")

            except Exception as e:
                print(f"Error fetching medical record for {patient['first_name']} {patient['last_name']}: {e}")

# Call the function
show_medical_records()
