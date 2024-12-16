from web3 import Web3

METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

if web3.is_connected():
    print("Connected to Ethereum network!")
    
    # Print the current user's Ethereum address (first account)
    if web3.eth.accounts:
        current_user = web3.eth.accounts[0]
        print(f"Current user (address): {current_user}")
    else:
        print("No accounts found.")
else:
    print("Failed to connect to Ethereum network.")
