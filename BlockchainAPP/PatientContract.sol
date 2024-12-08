// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientContract {

    struct Patient {
        string firstName;
        string lastName;
        uint birthDate;
        string addressDetails;
        address patientAddress;
        string[] medicalHistory;
    }

    mapping(address => Patient) public patients;

    // Register a patient
    function registerPatient(
        string memory _firstName,
        string memory _lastName,
        uint _birthDate,
        string memory _addressDetails
    ) public {
        require(bytes(patients[msg.sender].firstName).length == 0, "Patient already registered.");
        
        Patient storage patient = patients[msg.sender];
        patient.firstName = _firstName;
        patient.lastName = _lastName;
        patient.birthDate = _birthDate;
        patient.addressDetails = _addressDetails;
        patient.patientAddress = msg.sender;
    }

    // Add or update a medical record
    function addOrUpdateRecord(string memory _recordHash) public {
        patients[msg.sender].medicalHistory.push(_recordHash);
    }

    // View a patient's medical records
    function viewMedicalRecord(address patientAddress) public view returns (string[] memory) {
        return patients[patientAddress].medicalHistory;
    }
}
