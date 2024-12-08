// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./PatientContract.sol";

contract DoctorContract {

    struct Doctor {
        string firstName;
        string lastName;
        string specialty;
        address doctorAddress;
    }

    mapping(address => Doctor) public doctors;
    mapping(address => mapping(address => bool)) public accessPermissions; // Mapping for access permissions

    // Register a doctor
    function registerDoctor(
        string memory _firstName,
        string memory _lastName,
        string memory _specialty
    ) public {
        require(bytes(doctors[msg.sender].firstName).length == 0, "Doctor already registered.");
        doctors[msg.sender] = Doctor({
            firstName: _firstName,
            lastName: _lastName,
            specialty: _specialty,
            doctorAddress: msg.sender
        });
    }

    // Authorize a doctor to access a patient's records
    function authorizeAccess(address doctorAddress) public {
        accessPermissions[msg.sender][doctorAddress] = true;
    }

    // Revoke a doctor's access to a patient's records
    function revokeAccess(address doctorAddress) public {
        accessPermissions[msg.sender][doctorAddress] = false;
    }

    // Modifier to check if the caller is an authorized doctor for a patient
    modifier onlyDoctor(address patientAddress) {
        require(accessPermissions[patientAddress][msg.sender], "You do not have permission to access this record.");
        _;
    }
}
