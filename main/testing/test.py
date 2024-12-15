from web3 import Web3
import json
import sys

# Connect to the Ethereum node (MetaMask or Ganache or other local nodes)
METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

# Check if connected
if web3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect to Ethereum network.")
    sys.exit(1)

# Function to register a patient
def register_patient(contract_address, contract_abi, first_name, last_name, birth_date, address_details):
    # Set up the contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    
    # Get the default account (or prompt user to enter one)
    sender_address = web3.eth.accounts[0]
    print(f"Using account: {sender_address}")
    try:            # Call the viewAllPatients function to get all patient addresses
        patient_addresses = contract.functions.viewAllPatients().call()
        if not patient_addresses:
            print("No patients found.")
        else:
            print("Patient addresses:")
            for address in patient_addresses:
                print(address)
        
    except Exception as e:
            print(f"An error occurred: {e}")

    
    # Create transaction
    try:
        tx_hash = contract.functions.registerPatient(
            first_name,
            last_name,
            int(birth_date),  # Convert birth date to uint256
            address_details
        ).transact({'from': sender_address})
        
        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"Transaction successful with hash: {tx_hash.hex()}")
        print(f"Transaction receipt: {receipt}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function
def main():
    # Hardcoded contract address and ABI
    contract_address = "0xd0F350b13465B5251bb03E4bbf9Fa1DbC4a378F3"  # Replace with your contract address
    contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_recordHash",
				"type": "string"
			}
		],
		"name": "addOrUpdateRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "doctorAddress",
				"type": "address"
			}
		],
		"name": "authorizeAccess",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_firstName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_specialty",
				"type": "string"
			}
		],
		"name": "registerDoctor",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_firstName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_lastName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_birthDate",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_addressDetails",
				"type": "string"
			}
		],
		"name": "registerPatient",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "doctorAddress",
				"type": "address"
			}
		],
		"name": "revokeAccess",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "accessPermissions",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "audits",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "action",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "recordHash",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "actionType",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "doctorAddresses",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
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
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "isDoctor",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
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
		"name": "isPatient",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "patientAddresses",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
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
		"name": "patients",
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
				"internalType": "uint256",
				"name": "birthDate",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "addressDetails",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "patientAddress",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "viewAllAudits",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "action",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "user",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "recordHash",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "actionType",
						"type": "string"
					}
				],
				"internalType": "struct ProjetDAPP.Audit[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
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
		"inputs": [],
		"name": "viewAllPatients",
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
				"name": "patientAddress",
				"type": "address"
			}
		],
		"name": "viewMedicalRecord",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_recordHash",
				"type": "string"
			}
		],
		"name": "viewRecordAudit",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "action",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "user",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "recordHash",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "actionType",
						"type": "string"
					}
				],
				"internalType": "struct ProjetDAPP.Audit[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
    
    # Get patient details from user input
    first_name = input("Enter patient's first name: ")
    last_name = input("Enter patient's last name: ")
    birth_date = input("Enter patient's birth date (YYYY-MM-DD): ")
    address_details = input("Enter patient's address details: ")


    # Register the patient
    register_patient(contract_address, contract_abi, first_name, last_name, birth_date, address_details)



if __name__ == "__main__":
    main()
