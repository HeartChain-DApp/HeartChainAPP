from web3 import Web3

# Ethereum node connection
METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

if not web3.is_connected():
    print("Unable to connect to Ethereum network.")
    exit()

print("Connected to Ethereum network.")

# Smart contract details
CONTRACT_ADDRESS = "..............................."  # Replace with your deployed contract address
ABI = []

# Connect to contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Fetch doctors and patients from the contract
def fetch_doctors():
    try:
        doctor_addresses = contract.functions.viewAllDoctors().call()
        print("Doctors:")
        for addr in doctor_addresses:
            doctor = contract.functions.doctors(addr).call()
            print(f"Address: {addr}, First Name: {doctor[0]}, Last Name: {doctor[1]}, Specialty: {doctor[2]}")
    except Exception as e:
        print(f"Error fetching doctors: {e}")

def fetch_patients():
    try:
        patient_addresses = contract.functions.viewAllPatients().call()
        print("Patients:")
        for addr in patient_addresses:
            patient = contract.functions.patients(addr).call()
            print(f"Address: {addr}, First Name: {patient[0]}, Last Name: {patient[1]}, Birth Date: {patient[2]}, Ethereum Address: {addr}")
    except Exception as e:
        print(f"Error fetching patients: {e}")

if __name__ == "__main__":
    fetch_doctors()
    fetch_patients()
