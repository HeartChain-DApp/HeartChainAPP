// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditContract {

    struct Audit {
        uint timestamp;
        string action;
        address user;
        string recordHash;
        string actionType; // Creation, update, consultation, etc.
    }

    Audit[] public audits;

    // Record an audit action
    function recordAudit(string memory _action, string memory _actionType, address user, string memory _recordHash) public {
        Audit memory newAudit = Audit({
            timestamp: block.timestamp,
            action: _action,
            user: user,
            recordHash: _recordHash,
            actionType: _actionType
        });
        audits.push(newAudit);
    }

    // View all audits
    function viewAllAudits() public view returns (Audit[] memory) {
        return audits;
    }

    // View the audit of a specific medical record
    function viewRecordAudit(string memory _recordHash) public view returns (Audit[] memory) {
        uint count = 0;
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
}
