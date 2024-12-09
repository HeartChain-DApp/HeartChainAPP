from web3 import Web3

METAMASK_PROVIDER = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

if web3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect to Ethereum network.")
