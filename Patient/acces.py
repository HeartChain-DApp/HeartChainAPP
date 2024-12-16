from web3 import Web3

# Set up Web3 connection
METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

def manage_access_overall(patient_address, doctor_address, action):
    # Define contract ABI for authorize and revoke access functions
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
    
    # Define contract address
    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"
    
    # Connect to the smart contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Perform action based on the passed action parameter
    if action == 'authorize':
        tx_hash = contract.functions.authorizeAccess(doctor_address).transact({'from': patient_address})
        return tx_hash.hex()
        
    elif action == 'revoke':
        tx_hash = contract.functions.revokeAccess(doctor_address).transact({'from': patient_address})
        return tx_hash.hex()
    
    else:
        raise ValueError("Invalid action. Please use 'authorize' or 'revoke'.")
