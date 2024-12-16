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
        require(isDoctor[msg.sender], "Caller is not a registered doctor."); // Check if caller is a doctor
        require(isPatient[patientAddress], "Patient address is not registered."); // Check if patient is valid
        require(
            accessPermissions[patientAddress][msg.sender],
            "Doctor does not have permission to access this patient's records."
        ); // Check if permission is granted
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
function addOrUpdateRecord(
    address patientAddress,
    string memory diagnostic,
    string memory nurseName,
    string memory roomNumber,
    uint timeOfVisit
) public {
    // Check if the caller has permission to access the patient's records
    require(
        accessPermissions[patientAddress][msg.sender],
        "Access to this patient's records is not granted."
    );

    // Ensure the patient is valid
    require(isPatient[patientAddress], "The specified patient is not registered.");

    // Format the record details into a single string (optional: customize format)
    string memory recordDetails = string(
        abi.encodePacked(
            "Diagnostic: ", diagnostic,
            ", Nurse: ", nurseName,
            ", Room: ", roomNumber,
            ", Time: ", uint2str(timeOfVisit)
        )
    );

    // Add or update the medical record
    patients[patientAddress].medicalHistory.push(recordDetails);

    // Record the action in the audit log
    audits.push(Audit({
        timestamp: block.timestamp,
        action: "Record added/updated",
        user: msg.sender,
        recordHash: diagnostic, // Using the diagnostic field for auditing
        actionType: "Update"
    }));
}

// Helper function to convert uint to string
function uint2str(uint _i) internal pure returns (string memory) {
    if (_i == 0) {
        return "0";
    }
    uint j = _i;
    uint len;
    while (j != 0) {
        len++;
        j /= 10;
    }
    bytes memory bstr = new bytes(len);
    uint k = len;
    while (_i != 0) {
        k = k - 1;
        uint8 temp = (48 + uint8(_i - _i / 10 * 10));
        bytes1 b1 = bytes1(temp);
        bstr[k] = b1;
        _i /= 10;
    }
    return string(bstr);
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
    function listPatientsFollowingDoctor(address doctorAddress) public view returns (address[] memory) {
        require(isDoctor[doctorAddress], "Address is not a registered doctor.");
        
        uint patientCount = 0;
        
        // Count the number of patients who follow this doctor
        for (uint i = 0; i < patientAddresses.length; i++) {
            if (accessPermissions[patientAddresses[i]][doctorAddress]) {
                patientCount++;
            }
        }

        address[] memory followingPatients = new address[](patientCount);
        uint index = 0;
        
        // Collect the addresses of patients who follow this doctor
        for (uint i = 0; i < patientAddresses.length; i++) {
            if (accessPermissions[patientAddresses[i]][doctorAddress]) {
                followingPatients[index] = patientAddresses[i];
                index++;
            }
        }

        return followingPatients;
    }
}