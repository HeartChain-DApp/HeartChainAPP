from web3 import Web3
import json

# Connect to the Ethereum provider (e.g., Hardhat or your local Ethereum node)
METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Replace with your Hardhat provider
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

# Check if the connection is successful
if not web3.is_connected():
    print("Connection failed!")
    exit()
else:
    print("Connected to Ethereum network!")

# Define the contract ABI and address
contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "_firstName", "type": "string"},
            {"internalType": "string", "name": "_lastName", "type": "string"},
            {"internalType": "uint256", "name": "_birthDate", "type": "uint256"},
            {"internalType": "string", "name": "_addressDetails", "type": "string"}
        ],
        "name": "registerPatient",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
contract_address = "0x71bE63f3384f5fb98995898A86B02Fb2426c5788"  # Replace with your contract's address

# Set up the account and private key
private_key = "0x701b615bbdfb9de65240bc28bd21bbc0d996645a3dd57e7b12bc2bdf6f192c82"  # Replace with your private key

# Get account using the correct method for Web3 7.x
account = web3.eth.account.from_key(private_key)

# Define the sender's address
sender_address = account.address
print(f"Using account: {sender_address}")

# Create the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Define the input values for the patient
first_name = "John"
last_name = "Doe"
birth_date = 1234567890  # Example birth date as timestamp
address_details = "123 Main St, Springfield"

# Prepare the transaction
transaction = contract.functions.registerPatient(first_name, last_name, birth_date, address_details).build_transaction({
    'chainId': 1337,  # Replace with the correct chain ID for Hardhat (1337 by default)
    'gas': 2000000,  # Estimate gas limit
    'gasPrice': web3.to_wei('20', 'gwei'),  # Gas price (adjust based on network conditions)
    'nonce': web3.eth.get_transaction_count(sender_address),  # Nonce to prevent replay attacks
})

# Sign the transaction
signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

# Wait for the transaction receipt (confirmation)
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

# Check the receipt for successful transaction status
if transaction_receipt['status'] == 1:
    print("Patient registered successfully!")
else:
    print("Transaction failed!")
