import customtkinter as ctk
from web3 import Web3
from tkinter import messagebox

# Web3 setup (Replace with your actual provider URL)
METAMASK_PROVIDER = "http://127.0.0.1:8545"  # Your MetaMask provider
web3 = Web3(Web3.HTTPProvider(METAMASK_PROVIDER))

# Contract details (Replace with your actual contract address and ABI)
contract_address = "0x4826533B4897376654Bb4d4AD88B7faFD0C98528"  # Replace with your contract address
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_surname",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_password",
				"type": "string"
			}
		],
		"name": "signUpWithPassword",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "surname",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "generatedKey",
				"type": "string"
			}
		],
		"name": "UserSignedUp",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_userAddress",
				"type": "address"
			}
		],
		"name": "getUserInfo",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
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
				"name": "_userAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_key",
				"type": "string"
			}
		],
		"name": "login",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Set up contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to handle sign-up
def sign_up():
    name = name_entry.get()
    surname = surname_entry.get()
    password = password_entry.get()
    account_address = address_entry.get()
    private_key = private_key_entry.get()

    if not name or not surname or not password or not account_address or not private_key:
        messagebox.showerror("Error", "All fields must be filled.")
        return

    try:
        # Send transaction to contract for sign-up using transact()
        transaction = contract.functions.signUpWithPassword(name, surname, password).transact({
            'from': account_address,  # The address initiating the transaction
        })

        # Display success message with transaction hash
        messagebox.showinfo("Success", f"Sign-up successful! Transaction hash: {transaction.hex()}")
    except Exception as e:
        messagebox.showerror("Error", f"Error signing up: {str(e)}")

# Function to handle log-in
def log_in():
    user_address = address_entry.get()
    user_key = key_entry.get()

    if not user_address or not user_key:
        messagebox.showerror("Error", "All fields must be filled.")
        return

    try:
        # Call the contract's login function
        is_valid = contract.functions.login(user_address, user_key).call()

        if is_valid:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid login credentials.")
    except Exception as e:
        messagebox.showerror("Error", f"Error logging in: {str(e)}")

# Set up the main window
root = ctk.CTk()

root.title("Web3 Sign Up / Log In")

# Set window size
root.geometry("400x500")

# Create UI components for sign-up
name_label = ctk.CTkLabel(root, text="Name:")
name_label.pack(pady=5)
name_entry = ctk.CTkEntry(root)
name_entry.pack(pady=5)

surname_label = ctk.CTkLabel(root, text="Surname:")
surname_label.pack(pady=5)
surname_entry = ctk.CTkEntry(root)
surname_entry.pack(pady=5)

password_label = ctk.CTkLabel(root, text="Password:")
password_label.pack(pady=5)
password_entry = ctk.CTkEntry(root, show="*")
password_entry.pack(pady=5)

address_label = ctk.CTkLabel(root, text="Account Address:")
address_label.pack(pady=5)
address_entry = ctk.CTkEntry(root)
address_entry.pack(pady=5)

private_key_label = ctk.CTkLabel(root, text="Private Key:")
private_key_label.pack(pady=5)
private_key_entry = ctk.CTkEntry(root, show="*")
private_key_entry.pack(pady=5)

sign_up_button = ctk.CTkButton(root, text="Sign Up", command=sign_up)
sign_up_button.pack(pady=20)

# Log In section
key_label = ctk.CTkLabel(root, text="Generated Key:")
key_label.pack(pady=5)
key_entry = ctk.CTkEntry(root)
key_entry.pack(pady=5)

log_in_button = ctk.CTkButton(root, text="Log In", command=log_in)
log_in_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
