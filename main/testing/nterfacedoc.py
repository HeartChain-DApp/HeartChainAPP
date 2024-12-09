import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser
from web3 import Web3

# Connect to the Ethereum node (make sure MetaMask is running)
METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Change to your MetaMask provider URL if needed
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

if not web3.is_connected():
    print("Unable to connect to Ethereum network.")
    sys.exit()

print("Connected to Ethereum network.")

# Smart contract details
CONTRACT_ADDRESS = "0x95bD8D42f30351685e96C62EDdc0d0613bf9a87A"  # Replace with your deployed contract address
ABI = [
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
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# PyQt5 Window
class ContractApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Doctor & Patient Details")
        self.setGeometry(100, 100, 800, 600)
        
        self.layout = QVBoxLayout()

        # Buttons
        self.fetch_doctors_button = QPushButton("Fetch All Doctor Details", self)
        self.fetch_doctors_button.clicked.connect(self.fetch_doctor_details)
        self.layout.addWidget(self.fetch_doctors_button)

        self.fetch_patients_button = QPushButton("Fetch All Patient Details", self)
        self.fetch_patients_button.clicked.connect(self.fetch_patient_details)
        self.layout.addWidget(self.fetch_patients_button)

        # Text Browser for displaying results
        self.results_browser = QTextBrowser(self)
        self.layout.addWidget(self.results_browser)

        self.setLayout(self.layout)

        # Fetch all doctors and patients automatically at the start
        self.fetch_doctor_details()
        self.fetch_patient_details()

    def fetch_doctor_details(self):
        try:
            doctor_addresses = contract.functions.viewAllDoctors().call()
            if doctor_addresses:
                result_text = "Doctors List:\n"
                for doctor_address in doctor_addresses:
                    doctor = contract.functions.doctors(doctor_address).call()
                    result_text += f"\nDoctor Address: {doctor_address}\n"
                    result_text += f"First Name: {doctor[0]}\n"
                    result_text += f"Last Name: {doctor[1]}\n"
                    result_text += f"Specialty: {doctor[2]}\n"
                self.results_browser.setText(result_text)
            else:
                self.results_browser.setText("No doctors found.")
        except Exception as e:
            self.results_browser.setText(f"Error fetching doctor details: {e}")

    def fetch_patient_details(self):
        try:
            # Fetch all patient addresses from the contract
            patient_addresses = contract.functions.viewAllPatients().call()
            
            if not patient_addresses:
                self.results_browser.setText("No patients found.")
                return
            
            result_text = "Patients List:\n"
            
            # Loop through each patient address
            for patient_address in patient_addresses:
                # Fetch patient data using the address
                patient = contract.functions.patients(patient_address).call()

                # Debugging: Print the raw patient data to inspect
                print(f"Raw patient data for {patient_address}: {patient}")

                # Ensure that the patient data exists and has the expected structure
                if len(patient) >= 6:  # We expect at least 6 elements (first name, last name, etc.)
                    first_name = patient[0] if patient[0] else "N/A"
                    last_name = patient[1] if patient[1] else "N/A"
                    birth_date = patient[2] if patient[2] else "N/A"
                    address_details = patient[3] if patient[3] else "N/A"
                    medical_history = ', '.join(patient[5]) if patient[5] and len(patient[5]) > 0 else "No medical history available"

                    result_text += f"\nPatient Address: {patient_address}\n"
                    result_text += f"First Name: {first_name}\n"
                    result_text += f"Last Name: {last_name}\n"
                    result_text += f"Birth Date: {birth_date}\n"
                    result_text += f"Address: {address_details}\n"
                    result_text += f"Medical History: {medical_history}\n"
                else:
                    result_text += f"Error fetching details for patient address: {patient_address} (data incomplete)\n"

            self.results_browser.setText(result_text)

        except Exception as e:
            self.results_browser.setText(f"Error fetching patient details: {e}")



# Run the PyQt5 application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContractApp()
    window.show()
    sys.exit(app.exec_())
