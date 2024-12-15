from web3 import Web3

METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

if not web3.is_connected():
    print("Connection failed!")
    exit()
else:
    print("Connected to Ethereum network!")

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
contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"

private_key = "0x701b615bbdfb9de65240bc28bd21bbc0d996645a3dd57e7b12bc2bdf6f192c82"
account = web3.eth.account.from_key(private_key)

sender_address = account.address
print(f"Using account: {sender_address}")

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

first_name = "John"
last_name = "Doe"
birth_date = 1234567890
address_details = "123 Main St, Springfield"

transaction = contract.functions.registerPatient(first_name, last_name, birth_date, address_details).transact({
    'from': sender_address,
})

transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction)

if transaction_receipt['status'] == 1:
    print("Patient registered successfully!")
else:
    print("Transaction failed!")
