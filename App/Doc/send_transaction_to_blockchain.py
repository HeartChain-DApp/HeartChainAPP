from web3 import Web3

def send_transaction_to_blockchain(patient_address, diagnostic, nurse_name, room_number, time_of_visit):
    # Contract ABI and address
    contractabi = [{
        "inputs": [
            {"internalType": "address", "name": "patientAddress", "type": "address"},
            {"internalType": "string", "name": "diagnostic", "type": "string"},
            {"internalType": "string", "name": "nurseName", "type": "string"},
            {"internalType": "string", "name": "roomNumber", "type": "string"},
            {"internalType": "uint256", "name": "timeOfVisit", "type": "uint256"}
        ],
        "name": "addOrUpdateRecord",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"  # Your smart contract address
    METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Make sure your Ethereum node is running here
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    # Check if web3 is connected
    if not web3.is_connected():
        print("Failed to connect to the Ethereum provider.")
        return

    print("Connected to the Ethereum provider.")

    # Set up the contract object
    contract = web3.eth.contract(address=contract_address, abi=contractabi)
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Your private key
    account = web3.eth.account.from_key(private_key)
    sender_address = account.address

    # Send the transaction to the Ethereum network
    try:
        # Ensure the time_of_visit is an integer (because we can't send a string for uint256)
        time_of_visit = int(time_of_visit)

        # Prepare the transaction
        transaction = contract.functions.addOrUpdateRecord(
            patient_address, diagnostic, nurse_name, room_number, time_of_visit
        ).transact({'from': sender_address})

        # Wait for transaction receipt to confirm
        receipt = web3.eth.waitForTransactionReceipt(transaction)
        print(f"Transaction successful! Hash: {receipt.transactionHash.hex()}")

    except Exception as e:
        print(f"Error sending transaction: {str(e)}")
