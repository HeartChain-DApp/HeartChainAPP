import json
from web3 import Web3

def fetch_and_save_doctor_data():
    METAMASK_PROVIDER = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    if not web3.is_connected():
        print("Failed to connect to the provider.")
        return []

    print("Connected to the Ethereum provider.")

    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"
    contract_abi = [
       {
            "inputs": [],
            "name": "viewAllDoctors",
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
            "name": "doctors",
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
                    "internalType": "string",
                    "name": "specialty",
                    "type": "string"
                },
                {
                    "internalType": "address",
                    "name": "doctorAddress",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
    ]

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    def fetch_doctors():
        try:
            doctors = contract.functions.viewAllDoctors().call()
            return doctors
        except Exception as e:
            print(f"Error fetching doctors: {e}")
            return []

    def fetch_doctor_details(doctor_address):
        try:
            doctor_details = contract.functions.doctors(doctor_address).call()
            return doctor_details
        except Exception as e:
            print(f"Error fetching details for doctor {doctor_address}: {e}")
            return None

    doctors = fetch_doctors()
    doctors_data = []

    if doctors:
        for doctor_address in doctors:
            details = fetch_doctor_details(doctor_address)
            if details:
                doctor_info = {
                    "firstName": details[0],
                    "lastName": details[1],
                    "specialty": details[2],
                    "doctorAddress": details[3]
                }
                doctors_data.append(doctor_info)

    return doctors_data

