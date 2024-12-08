// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProjetDAPP {

    // Data structures for each entity
    struct Patient {
        string firstName;
        string lastName;
        uint birthDate;
        string addressDetails;
        address patientAddress;
        string[] medicalHistory; // List of hashes of medical records
    }

    struct Doctor {
        string firstName;
        string lastName;
        string specialty;
        address doctorAddress;
    }

    struct Audit {
        uint timestamp;
        string action;
        address user; // User who performed the action
        string recordHash;
        string actionType; // Creation, update, consultation, etc.
    }

    // Mappings for patients, doctors, and audits
    mapping(address => Patient) public patients;
    mapping(address => Doctor) public doctors;
    mapping(address => mapping(address => bool)) public accessPermissions; // Mapping to store access permissions
    Audit[] public audits;

    // Lists for all registered patients and doctors
    address[] public patientAddresses;
    address[] public doctorAddresses;

    // Flags to track if an address is registered as a patient or doctor
    mapping(address => bool) public isPatient;
    mapping(address => bool) public isDoctor;

    // Modifier to check if the caller is an authorized doctor
    modifier onlyDoctor(address patientAddress) {
        require(accessPermissions[patientAddress][msg.sender], "You do not have permission to access this record.");
        _;
    }

    // Modifier to check if the caller is the patient
    modifier onlyPatient(address patientAddress) {
        require(msg.sender == patientAddress, "You are not the patient.");
        _;
    }

    // Function to register a patient
    function registerPatient(
        string memory _firstName,
        string memory _lastName,
        uint _birthDate,
        string memory _addressDetails
    ) public {
        require(!isPatient[msg.sender] && !isDoctor[msg.sender], "You are already registered as either a patient or a doctor.");
        
        Patient storage patient = patients[msg.sender];
        patient.firstName = _firstName;
        patient.lastName = _lastName;
        patient.birthDate = _birthDate;
        patient.addressDetails = _addressDetails;
        patient.patientAddress = msg.sender;
        
        // Mark the address as a patient
        isPatient[msg.sender] = true;
        patientAddresses.push(msg.sender);
        
        recordAudit("Patient registration", "Creation");
    }

    // Function to register a doctor
    function registerDoctor(
        string memory _firstName,
        string memory _lastName,
        string memory _specialty
    ) public {
        require(!isPatient[msg.sender] && !isDoctor[msg.sender], "You are already registered as either a patient or a doctor.");
        
        doctors[msg.sender] = Doctor({
            firstName: _firstName,
            lastName: _lastName,
            specialty: _specialty,
            doctorAddress: msg.sender
        });
        
        // Mark the address as a doctor
        isDoctor[msg.sender] = true;
        doctorAddresses.push(msg.sender);
    }

    // Function to authorize a doctor to access a patient's records
    function authorizeAccess(address doctorAddress) public onlyPatient(msg.sender) {
        accessPermissions[msg.sender][doctorAddress] = true;
        recordAudit("Access authorized", "Permission");
    }

    // Function to revoke a doctor's access to a patient's records
    function revokeAccess(address doctorAddress) public onlyPatient(msg.sender) {
        accessPermissions[msg.sender][doctorAddress] = false;
        recordAudit("Access revoked", "Permission");
    }

    // Function to add or update a medical record
    function addOrUpdateRecord(string memory _recordHash) public onlyDoctor(msg.sender) {
        patients[msg.sender].medicalHistory.push(_recordHash);
        recordAudit("Record updated", "Update");
    }

    // Function to view a patient's medical records
    function viewMedicalRecord(address patientAddress) public view onlyDoctor(patientAddress) returns (string[] memory) {
        return patients[patientAddress].medicalHistory;
    }

    // Function to record an audit action
    function recordAudit(string memory _action, string memory _actionType) private {
        Audit memory newAudit = Audit({
            timestamp: block.timestamp,
            action: _action,
            user: msg.sender,
            recordHash: "",
            actionType: _actionType
        });
        audits.push(newAudit);
    }

    // Function to view all audits
    function viewAllAudits() public view returns (Audit[] memory) {
        return audits;
    }

    // Function to view the audit of a specific medical record
    function viewRecordAudit(string memory _recordHash) public view returns (Audit[] memory) {
        uint count = 0;
        // Count the number of audits for this specific record
        for (uint i = 0; i < audits.length; i++) {
            if (keccak256(abi.encodePacked(audits[i].recordHash)) == keccak256(abi.encodePacked(_recordHash))) {
                count++;
            }
        }
        
        Audit[] memory result = new Audit[](count);
        uint j = 0;
        for (uint i = 0; i < audits.length; i++) {
            if (keccak256(abi.encodePacked(audits[i].recordHash)) == keccak256(abi.encodePacked(_recordHash))) {
                result[j] = audits[i];
                j++;
            }
        }
        return result;
    }

    // Function to view all registered patients
    function viewAllPatients() public view returns (address[] memory) {
        return patientAddresses;
    }

    // Function to view all registered doctors
    function viewAllDoctors() public view returns (address[] memory) {
        return doctorAddresses;
    }
}
