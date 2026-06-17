"""Compila y despliega AuditoriaBecas.sol en Polygon Amoy, y guarda la direccion en .env.

Uso:
    python contracts/deploy.py

Requisitos:
- .env con AMOY_RPC_URL y PRIVATE_KEY (la wallet debe tener POL de prueba del faucet).
- py-solc-x instalado (esta en requirements.txt).

Si la wallet no tiene fondos, el script avisa y no hace nada (no rompe).
"""
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from web3 import Web3
import solcx

RUTA_ENV = ".env"
RUTA_SOL = "contracts/AuditoriaBecas.sol"
VERSION_SOLC = "0.8.20"


def _compilar():
    try:
        solcx.set_solc_version(VERSION_SOLC)
    except Exception:
        solcx.install_solc(VERSION_SOLC)
        solcx.set_solc_version(VERSION_SOLC)
    fuente = Path(RUTA_SOL).read_text(encoding="utf-8")
    compilado = solcx.compile_source(
        fuente, output_values=["abi", "bin"], solc_version=VERSION_SOLC
    )
    clave = [k for k in compilado if k.endswith(":AuditoriaBecas")][0]
    return compilado[clave]["abi"], compilado[clave]["bin"]


def _guardar_address_en_env(address):
    texto = Path(RUTA_ENV).read_text(encoding="utf-8")
    if re.search(r"^CONTRACT_ADDRESS=.*$", texto, flags=re.MULTILINE):
        texto = re.sub(r"^CONTRACT_ADDRESS=.*$", f"CONTRACT_ADDRESS={address}",
                       texto, flags=re.MULTILINE)
    else:
        texto += f"\nCONTRACT_ADDRESS={address}\n"
    Path(RUTA_ENV).write_text(texto, encoding="utf-8")


def main():
    load_dotenv()
    rpc = os.environ["AMOY_RPC_URL"]
    pk = os.environ["PRIVATE_KEY"]

    w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 30}))
    cuenta = w3.eth.account.from_key(pk)
    print(f"Wallet: {cuenta.address}")

    saldo = w3.eth.get_balance(cuenta.address)
    print(f"Saldo: {w3.from_wei(saldo, 'ether')} POL")
    if saldo == 0:
        print("\n  Esta wallet no tiene fondos. Pedi POL de prueba en un faucet de Amoy")
        print("  (ej: https://faucet.polygon.technology) pegando la direccion de arriba,")
        print("  esperá a que llegue y volvé a correr este script.")
        return

    abi, bytecode = _compilar()
    contrato = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = contrato.constructor().build_transaction({
        "from": cuenta.address,
        "nonce": w3.eth.get_transaction_count(cuenta.address),
        "gas": 500000,
        "gasPrice": w3.eth.gas_price,
    })
    firmada = cuenta.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(firmada.rawTransaction)
    print(f"Desplegando... tx: {tx_hash.hex()}")
    recibo = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    address = recibo.contractAddress
    print(f"Contrato desplegado en: {address}")
    print(f"Ver en: https://amoy.polygonscan.com/address/{address}")

    _guardar_address_en_env(address)
    print("CONTRACT_ADDRESS guardado en .env")


if __name__ == "__main__":
    main()
