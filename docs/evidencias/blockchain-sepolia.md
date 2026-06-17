# Evidencia — Registro en blockchain (Ethereum Sepolia)

El smart contract `AuditoriaBecas` fue compilado y desplegado en la testnet **Ethereum Sepolia**,
y se registró una decisión real (certificado de auditoría) de forma verificable por cualquiera.

## Contrato desplegado

- **Dirección:** `0xa37E9b370840F14f5E5C69Ff7B7119eCE3034176`
- **Explorer:** https://sepolia.etherscan.io/address/0xa37E9b370840F14f5E5C69Ff7B7119eCE3034176
- **Bloque de despliegue:** 11081784

## Transacción de auditoría registrada

Decisión registrada: postulante elegible bajo la regla
`SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`.

- **Hash de la decisión (sha256):** `0xb6e14cbddd054ceae4585471827ba0fea6e3156809cbb6193223caea6296fe31`
- **Transacción on-chain:** https://sepolia.etherscan.io/tx/0x34b381d426e9aaba2b3b1aba7b37b3d863563affbab54d0aee2b3367c8b01e44

## Qué demuestra

- El hash `hash(datos + regla + resultado)` quedó **sellado de forma inmutable** en la blockchain:
  nadie puede alterar la decisión después de tomada.
- Cualquiera puede verificar en el explorer que esa decisión existió y cuándo se registró.
- El sistema funciona también en modo `fallback` local (sin red), por lo que la demo nunca se
  interrumpe; con `.env` configurado (RPC + clave + dirección del contrato) opera on-chain real.
