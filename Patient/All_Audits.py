import json
from web3 import Web3
from datetime import datetime

def fetch_audit_logs():
    # Define the provider URL for MetaMask (or your local Ethereum node)
    METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Replace with your provider
    web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

    # Ensure the connection is successful
    if not web3.is_connected():
        print("Failed to connect to the provider.")
        return []

    # Contract ABI and address (replace with actual values)
    contract_address = "0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB"  # Replace with your contract address
    contract_abi = [
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
        }
    ]

    # Initialize contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Fetch the audit logs
    try:
        audit_logs = contract.functions.viewAllAudits().call()
    except Exception as e:
        print(f"Error fetching audit logs: {e}")
        return []

    formatted_audit_logs = []
    if audit_logs:
        for audit in audit_logs:
            timestamp = datetime.utcfromtimestamp(audit[0]).strftime('%Y-%m-%d %H:%M:%S')
            action = audit[1]
            user = audit[2]
            record_hash = audit[3] if audit[3] else "N/A"
            action_type = audit[4]
            
            formatted_audit_logs.append({
                "timestamp": timestamp,
                "action": action,
                "user": user,
                "record_hash": record_hash,
                "action_type": action_type
            })

    return formatted_audit_logs
