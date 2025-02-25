// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AegisCredit {
    struct CreditSnapshot {
        address user;
        uint256 creditScore;
        uint256 timestamp;
        string reportHash;
    }

    mapping(address => CreditSnapshot) public snapshots;
    mapping(bytes32 => CreditSnapshot) public snapshotByFingerprint; // Fingerprint-based mapping

    event CreditSnapshotStored(address indexed user, uint256 creditScore, uint256 timestamp, string reportHash, bytes32 fingerprint);

    function storeCreditSnapshot(uint256 _creditScore, string memory _reportHash, string memory fingerprint) public {
        bytes32 fingerprintHash = keccak256(abi.encodePacked(fingerprint));

        // ✅ Check if the fingerprint already exists
        require(bytes(snapshotByFingerprint[fingerprintHash].reportHash).length == 0, "Duplicate submission detected");

        snapshots[msg.sender] = CreditSnapshot(msg.sender, _creditScore, block.timestamp, _reportHash);
        snapshotByFingerprint[fingerprintHash] = CreditSnapshot(msg.sender, _creditScore, block.timestamp, _reportHash);

        emit CreditSnapshotStored(msg.sender, _creditScore, block.timestamp, _reportHash, fingerprintHash);
    }

    function getCreditSnapshotByFingerprint(string memory fingerprint) public view returns (CreditSnapshot memory) {
        bytes32 fingerprintHash = keccak256(abi.encodePacked(fingerprint));
        require(bytes(snapshotByFingerprint[fingerprintHash].reportHash).length > 0, "Snapshot not found");
        return snapshotByFingerprint[fingerprintHash];
    }
}
