from web3 import Web3
from All_Doc import fetch_and_save_doctor_data

METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

def doct_addrs():
    doctors = fetch_and_save_doctor_data()
    doctor_addresses = [doctor['doctorAddress'] for doctor in doctors]
    return doctor_addresses
    

