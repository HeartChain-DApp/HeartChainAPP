from web3 import Web3

def show_medical_records():
    # Define the target patient address
    target_patient_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    
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

        # Return medical records
        if not medical_records:
            return f"No medical records found for the patient with address {target_patient_address}."
        else:
            return medical_records

    except Exception as e:
        return f"Error fetching medical records for patient with address {target_patient_address}: {e}"

# Call the function and return the result
