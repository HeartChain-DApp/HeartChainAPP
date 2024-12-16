from web3 import Web3



def fetch_patients_following_doctor(index):
    """Fetch and return the list of patients following a doctor using the doctor's index."""
    # Initialize Web3 connection
    METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Replace with your provider
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    # Ensure the connection is successful
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum provider.")

    # Contract details
    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"  # Replace with your contract address
    contract_abi = [
        {
            "inputs": [
                {"internalType": "address", "name": "doctorAddress", "type": "address"}
            ],
            "name": "listPatientsFollowingDoctor",
            "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "name": "patients",
            "outputs": [
                {"internalType": "string", "name": "firstName", "type": "string"},
                {"internalType": "string", "name": "lastName", "type": "string"},
                {"internalType": "uint256", "name": "birthDate", "type": "uint256"},
                {"internalType": "string", "name": "addressDetails", "type": "string"},
                {"internalType": "address", "name": "patientAddress", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "name": "doctorAddresses",
            "outputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    # Initialize the contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    try:
        # Retrieve the doctor's address using the index
        doctor_address = contract.functions.doctorAddresses(index).call()

        # Call the contract function to get the list of patient addresses
        patient_addresses = contract.functions.listPatientsFollowingDoctor(doctor_address).call()

        # If no patients are found, return an empty list
        if not patient_addresses:
            return []

        # List to hold patient details
        patient_details = []

        # Fetch details for each patient
        for patient_address in patient_addresses:
            details = contract.functions.patients(patient_address).call()
            first_name = details[0]
            last_name = details[1]
            birth_date = datetime.utcfromtimestamp(details[2]).strftime('%Y-%m-%d')
            address_details = details[3]
            patient_address = details[4]

            # Append patient data to the list
            patient_details.append({
                "first_name": first_name,
                "last_name": last_name,
                "birth_date": birth_date,
                "address_details": address_details,
                "patient_address": patient_address
            })

        return patient_details

    except Exception as e:
        print(f"Error fetching patient data: {e}")
        return []


def show_medical_records():
    # Define the target patient address
    target_patient_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    
    # Fetch patients following the doctor (though it's not needed here)
    patients = fetch_patients_following_doctor(0)

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

    # Directly use the target patient address to fetch medical records
    try:
        medical_records = contract.functions.viewMedicalRecord(target_patient_address).call()

        if not medical_records:
            print(f"No medical records found for the patient with address {target_patient_address}.")
        else:
            print(f"Medical records for the patient with address {target_patient_address}:")
            for record in medical_records:
                print(record)

    except Exception as e:
        print(f"Error fetching medical records for patient with address {target_patient_address}: {e}")

show_medical_records()
