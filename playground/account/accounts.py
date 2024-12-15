import json
from web3 import Web3

# Connect to Hardhat's local JSON-RPC server
hardhat_url = "http://127.0.0.1:8545/"
web3 = Web3(Web3.HTTPProvider(hardhat_url))

# Check if connected
if not web3.is_connected():
    print("Error: Unable to connect to Hardhat RPC server.")
    exit()

# Fetch accounts
accounts = web3.eth.accounts
print("Accounts:")

# Path to the JSON file
json_file_path = "accounts.json"

# Read the existing JSON data (if any)
try:
    with open(json_file_path, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []  # If the file doesn't exist, initialize an empty list

# Update the accounts list in the JSON file with new accounts
for i, account in enumerate(accounts):
    
    # Create an entry for each account in the JSON data
    account_data = {
        "account": account,
        "private_key": web3.eth.account.privateKeyToAccount(account).privateKey.hex(),
    }
    data.append(account_data)

# Write the updated data back into the JSON file
with open(json_file_path, "w") as f:
    json.dump(data, f, indent=4)

print(f"Accounts have been saved to {json_file_path}")
