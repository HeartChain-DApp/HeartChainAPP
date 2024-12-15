from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget)
import sys
import os
from web3 import Web3

# Load environment variable

CONTRACT_ADDRESS = "0x5e17b14ADd6c386305A32928F985b29bbA34Eff5"

CONTRACT_ABI = [
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
# Initialize web3
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not web3.is_connected():
    print("Web3 is not connected. Check your provider and network configuration.")

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Registration")
        self.setGeometry(100, 100, 800, 400)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_widget.setStyleSheet("background-color: #2c2c2c;")

        # Left side: Welcome label
        left_layout = QVBoxLayout()
        welcome_label = QLabel("Welcome")
        welcome_label.setStyleSheet("font-size: 36px; font-weight: bold; color: white;")
        left_layout.addWidget(welcome_label)
        left_layout.addStretch()

        # Right side: Input fields and Register button
        right_layout = QVBoxLayout()

        first_name_label = QLabel("First Name")
        first_name_label.setStyleSheet("color: white; font-size: 16px;")
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter your first name")
        self.first_name_input.setStyleSheet("background-color: #1c1c1c; color: #00bfff; padding: 5px; font-size: 16px; border: none;")

        last_name_label = QLabel("Last Name")
        last_name_label.setStyleSheet("color: white; font-size: 16px;")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter your last name")
        self.last_name_input.setStyleSheet("background-color: #1c1c1c; color: #00bfff; padding: 5px; font-size: 16px; border: none;")

        birth_date_label = QLabel("Birth Date")
        birth_date_label.setStyleSheet("color: white; font-size: 16px;")
        self.birth_date_input = QLineEdit()
        self.birth_date_input.setPlaceholderText("Enter your birth date (e.g., 19900101)")
        self.birth_date_input.setStyleSheet("background-color: #1c1c1c; color: #00bfff; padding: 5px; font-size: 16px; border: none;")

        address_details_label = QLabel("Address Details")
        address_details_label.setStyleSheet("color: white; font-size: 16px;")
        self.address_details_input = QLineEdit()
        self.address_details_input.setPlaceholderText("Enter your address details")
        self.address_details_input.setStyleSheet("background-color: #1c1c1c; color: #00bfff; padding: 5px; font-size: 16px; border: none;")

        register_button = QPushButton("Register")
        register_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        register_button.clicked.connect(self.handle_register)

        # Add widgets to right layout
        right_layout.addWidget(first_name_label)
        right_layout.addWidget(self.first_name_input)
        right_layout.addWidget(last_name_label)
        right_layout.addWidget(self.last_name_input)
        right_layout.addWidget(birth_date_label)
        right_layout.addWidget(self.birth_date_input)
        right_layout.addWidget(address_details_label)
        right_layout.addWidget(self.address_details_input)
        right_layout.addWidget(register_button)
        right_layout.addStretch()

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=2)

        main_widget.setLayout(main_layout)

    def handle_register(self):
        # Get input values
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        birth_date = self.birth_date_input.text()
        address_details = self.address_details_input.text()

        # Validate inputs
        if not (first_name and last_name and birth_date.isdigit() and address_details):
            print("Please fill in all fields correctly.")
            return

        # Ensure address_details is a valid string
        if not isinstance(address_details, str) or not address_details.strip():
            print("Invalid address details.")
            return

        try:
            # Call the smart contract function
            tx_hash = contract.functions.registerPatient(
                first_name, 
                last_name, 
                int(birth_date), 
                address_details
            ).transact({'from': web3.eth.default_account or '0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba'})

            
            print(f"Transaction hash: {tx_hash}")
            
        except Exception as e:
            print(f"An error occurred: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())
