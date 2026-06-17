// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditoriaBecas {
    event DecisionRegistrada(bytes32 indexed hashDecision, uint256 timestamp, address emisor);

    mapping(bytes32 => uint256) public registros;

    function registrar(bytes32 hashDecision) external {
        require(registros[hashDecision] == 0, "Ya registrado");
        registros[hashDecision] = block.timestamp;
        emit DecisionRegistrada(hashDecision, block.timestamp, msg.sender);
    }

    function existe(bytes32 hashDecision) external view returns (bool) {
        return registros[hashDecision] != 0;
    }
}
