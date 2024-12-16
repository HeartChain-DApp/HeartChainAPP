from web3   import Web3
from docaddress import doct_addrs

def doc_details(docadress):
    METAMASK_PROVIDER = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    contract_abi=[{
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
	},]
    contract_address="0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    try:
        doctor_details = contract.functions.doctors(docadress).call()
        print(doctor_details)
        return doctor_details
        
    except Exception as e:
        print(f"Error fetching details for doctor {docadress}: {e}")
        return None
    

doc_details("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")