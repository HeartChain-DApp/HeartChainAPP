import tkinter as tk
from tkinter import messagebox
from flask import Flask, request
import threading
import webbrowser

# Flask Backend
app = Flask(__name__)
selected_account = None  # To store the authenticated Ethereum account

# HTML template with Web3.js for Metamask connection
metamask_html = """<!DOCTYPE html>
<html>
<head>
    <title>Metamask Authentication</title>
    <script src="https://cdn.jsdelivr.net/npm/web3/dist/web3.min.js"></script>
    <script>
        async function connectMetamask() {
            if (window.ethereum) {
                try {
                    // Request account access
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    const account = accounts[0];
                    const chainId = await ethereum.request({ method: 'eth_chainId' }); // Get the chain ID
                    const provider = window.ethereum.isMetaMask ? 'MetaMask' : 'Other'; // Identify the provider
                    
                    // You can generate or fetch an authentication token and timestamp if necessary
                    const auth_token = 'example_auth_token';  // This can be a generated token or signature
                    const timestamp = new Date().toISOString(); // Get the current timestamp
                    
                    // Redirect to Flask with the selected account and additional data
                    window.location.href = "/authenticated?account=" + account +
                                           "&chain_id=" + chainId +
                                           "&provider=" + provider +
                                           "&auth_token=" + auth_token +
                                           "&timestamp=" + timestamp;
                } catch (error) {
                    alert("User denied account access.");
                }
            } else {
                alert("Metamask not detected. Please install Metamask.");
            }
        }
    </script>
</head>
<body>
    <h1>Metamask Authentication</h1>
    <button onclick="connectMetamask()">Connect Metamask</button>
</body>
</html>

"""

@app.route('/')
def index():
    return metamask_html  # Serve the Metamask connection page

@app.route('/authenticated')
def authenticated():
    """
    Handle the callback from the Metamask connection.
    """
    global selected_account
    selected_account = request.args.get('account')  # Retrieve account from query parameters
    chain_id = request.args.get('chain_id')  # Retrieve chain ID (if available)
    provider = request.args.get('provider')  # Retrieve wallet provider (MetaMask, etc.)
    auth_token = request.args.get('auth_token')  # Retrieve authentication token (if available)
    timestamp = request.args.get('timestamp')  # Retrieve timestamp of the authentication
    
    if selected_account:
        return f"Authentication successful! Account: {selected_account}, Chain ID: {chain_id}, Provider: {provider}, Token: {auth_token}, Timestamp: {timestamp}"
    return "Authentication failed."



def run_flask():
    """
    Start the Flask server in a separate thread.
    """
    app.run(port=5000)


# Tkinter Frontend
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login with Metamask")
        self.root.geometry("300x200")

        self.label = tk.Label(root, text="Login with Metamask", font=("Arial", 16))
        self.label.pack(pady=20)

        self.login_button = tk.Button(root, text="Login", command=self.authenticate_with_metamask)
        self.login_button.pack(pady=20)

        self.account_label = tk.Label(root, text="No account selected", font=("Arial", 12))
        self.account_label.pack(pady=20)

    def authenticate_with_metamask(self):
        """
        Open the browser for Metamask authentication.
        """
        url = "http://localhost:5000/"
        webbrowser.open(url)

        # Start polling for the authenticated account
        self.poll_for_account()

    def poll_for_account(self):
        """
        Poll for the authenticated account from the Flask server.
        """
        global selected_account
        if selected_account:
            self.account_label.config(text=f"Account: {selected_account}")
            messagebox.showinfo("Authentication Successful", f"Logged in as: {selected_account}")
        else:
            # Check again after 1 second
            self.root.after(1000, self.poll_for_account)


# Main Program
if __name__ == "__main__":
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Tkinter GUI
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
