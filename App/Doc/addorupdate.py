from listingfollowing import fetch_patients_following_doctor
from web3 import Web3

def addorupdate():
    overall = fetch_patients_following_doctor(0)
    patient_addresses = [patient.get('patient_address') for patient in overall if 'patient_address' in patient]

    if not patient_addresses:
        print("No patients found.")
        return

    print("Patients:")
    for i, address in enumerate(patient_addresses):
        print(f"{i}: {address}")

    try:
        choice = int(input(f"Choose a patient (0-{len(patient_addresses) - 1}): "))
        if choice < 0 or choice >= len(patient_addresses):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    patadress = patient_addresses[choice]

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
    contractadress = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"

    METAMASK_PROVIDER = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    if not web3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum provider.")

    print("Connected to the Ethereum provider.")
    contract = web3.eth.contract(address=contractadress, abi=contractabi)
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    account = web3.eth.account.from_key(private_key)
    sender_address = account.address

    diagnostic = "jomani"
    nurseName = "hamid"
    roomNumber = "121"
    timeOfVisit = 2112

    transaction = contract.functions.addOrUpdateRecord(
        patadress, diagnostic, nurseName, roomNumber, timeOfVisit
    ).transact({'from': sender_address})

    print(f"Transaction sent: {transaction.hex()}")

addorupdate()
