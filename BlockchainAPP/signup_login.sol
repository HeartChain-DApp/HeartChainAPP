// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UserAuthentication {

    // Struct to store user information
    struct User {
        string name;
        string surname;
        string password;
        string generatedKey;
    }

    // Mapping to store users by their address
    mapping(address => User) private users;

    // Event for successful sign up
    event UserSignedUp(address userAddress, string name, string surname, string generatedKey);

    // Function to sign up the user
    function signUpWithPassword(string memory _name, string memory _surname, string memory _password) public {
        require(bytes(_name).length > 0, "Name is required.");
        require(bytes(_surname).length > 0, "Surname is required.");
        require(bytes(_password).length > 0, "Password is required.");

        // Generate an 8-character key
        string memory generatedKey = generateRandomKey();

        // Store the user details
        users[msg.sender] = User({
            name: _name,
            surname: _surname,
            password: _password,
            generatedKey: generatedKey
        });

        // Emit event for successful sign up
        emit UserSignedUp(msg.sender, _name, _surname, generatedKey);
    }

    // Function to generate a random 8-character key (requires view)
    function generateRandomKey() private view returns (string memory) {
        bytes memory key = new bytes(8);
        bytes32 randomHash = keccak256(abi.encodePacked(block.timestamp, block.difficulty));

        // Ensure printable ASCII characters for key generation
        for (uint i = 0; i < 8; i++) {
            uint8 randomByte = uint8(uint(randomHash) >> (i * 8) & 0xFF);
            // Ensure printable ASCII characters between 32 (space) and 126 (~)
            key[i] = bytes1(32 + (randomByte % 95)); 
        }

        return string(key);
    }

    // Function to log in using address and the generated key
    function login(address _userAddress, string memory _key) public view returns (bool) {
        require(bytes(_key).length == 8, "Invalid key length. Key must be 8 characters.");

        // Check if the provided key matches the stored key
        if (keccak256(abi.encodePacked(users[_userAddress].generatedKey)) == keccak256(abi.encodePacked(_key))) {
            return true; // Login successful
        }

        return false; // Login failed
    }

    // Function to get user information (for debugging purposes)
    function getUserInfo(address _userAddress) public view returns (string memory, string memory, string memory) {
        return (
            users[_userAddress].name,
            users[_userAddress].surname,
            users[_userAddress].generatedKey
        );
    }
}
