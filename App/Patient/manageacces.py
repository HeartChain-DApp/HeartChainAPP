from web3 import Web3

METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

def manage_access_overall(patient_address, doctor_address, action):
    # Contract ABI for the functions we want to call (authorize and revoke)
    contract_abi = [{
        "inputs": [{"internalType": "address", "name": "doctorAddress", "type": "address"}],
        "name": "authorizeAccess",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "doctorAddress", "type": "address"}],
        "name": "revokeAccess",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }]

    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Ensure the action is valid
    if action == 'authorize':
        # Authorize the doctor by calling the contract function
        tx_hash = contract.functions.authorizeAccess(doctor_address).transact({'from': patient_address})
        print(f"Access authorized for doctor at {doctor_address}. Transaction hash: {tx_hash.hex()}")

    elif action == 'revoke':
        # Revoke the doctor's access by calling the contract function
        tx_hash = contract.functions.revokeAccess(doctor_address).transact({'from': patient_address})
        print(f"Access revoked for doctor at {doctor_address}. Transaction hash: {tx_hash.hex()}")

    else:
        # If the action is invalid, notify the user
        print("Invalid action. Please enter 'authorize' or 'revoke'.")
