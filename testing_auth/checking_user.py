import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from web3 import Web3

class MetaMaskApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Web3 to connect to the local Ethereum node
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        self.setWindowTitle("MetaMask Account Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Label to display the Ethereum account
        self.label = QLabel("Ethereum Account: Not connected", self)
        self.layout.addWidget(self.label)

        # Button to fetch the account
        self.button = QPushButton("Fetch Account", self)
        self.button.clicked.connect(self.fetch_account)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def fetch_account(self):
        # Check if Web3 is connected
        if self.w3.is_connected():
            # Get the first account (for example)
            account = self.w3.eth.accounts[0] if self.w3.eth.accounts else "No accounts found"
            self.label.setText(f"Ethereum Account: {account}")
        else:
            self.label.setText("Ethereum Node not connected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MetaMaskApp()
    window.show()
    sys.exit(app.exec_())
