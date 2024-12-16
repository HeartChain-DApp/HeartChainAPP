# HeartChainAPP

HeartChainAPP is a decentralized desktop application built using **CustomTkinter** for the graphical user interface and integrated with smart contracts for blockchain functionality. This project demonstrates how decentralized applications (DApps) can provide secure and efficient solutions for managing sensitive data, such as healthcare information.

---

## Getting Started

### 1. Clone the Project
Clone the project repository from GitHub:
```bash
git clone https://github.com/HeartChain-DApp/HeartChainAPP.git
```

### 2. Set Up Virtual Environment
Activate the virtual environment depending on your operating system:
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Update Smart Contract Address
Replace the contract address in the project with your deployed contract's address. This ensures the application can interact with the correct blockchain contract.

### 4. Install Hardhat
Install **Hardhat**, a development environment for Ethereum smart contracts:
```bash
npm install --save-dev hardhat
```

### 5. Initialize Hardhat
After installing Hardhat, initialize it in the project:
```bash
npx hardhat init
```

### 6. Run Hardhat Node
Once the initialization is successful, run the Hardhat local blockchain node:
```bash
npx hardhat node
```

---

## Project Structure
The project is divided into multiple directories, each serving a specific purpose:

### 1. **App**
This directory contains the main application code, including the graphical user interface (GUI) for both doctors and patients:
- **`doc.py`**: Starts the GUI for doctors.
- **`pat.py`**: Starts the GUI for patients.

Each file has corresponding advanced functions imported to handle specific tasks within the application.

### 2. **BlockchainDapp**
This directory contains the smart contracts written in Solidity. These contracts form the backbone of the decentralized functionality of the application.

### 3. **test**
Contains minimized functions to help test the connection between the application and the blockchain, including:
- Contract deployment.
- Hardhat integration.
- Basic smart contract interactions.

### 4. **playground**
A testing ground for experimenting with the contract’s functionality using terminal-based commands. Use this directory to validate contract behavior before integrating it with the application.

---

## Testing the GUI
To test the GUI functionality:
1. Run either `doc.py` or `pat.py` in the **App** directory.
2. Modify or extend the GUI as needed for your use case.

---

## Contributors
This project was developed by:
- **Abdelmajid Benjelloun**
- **Mohammed Aachabi**
- **Marouan Daghmoumi**

---

## License
This project is licensed under the MIT License. Feel free to use and modify it for your own purposes.

---

## Feedback
We welcome your feedback and contributions to make HeartChainAPP even better. Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/HeartChain-DApp/HeartChainAPP).

