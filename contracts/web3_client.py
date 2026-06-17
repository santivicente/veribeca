import os
import json
import hashlib
import time
from pathlib import Path

RUTA_FALLBACK = "contracts/fallback_ledger.json"
RUTA_ABI = "contracts/abi.json"


def calcular_hash(postulante, texto_regla, resultado):
    payload = json.dumps(
        {"postulante": postulante, "regla": texto_regla, "resultado": resultado},
        sort_keys=True, ensure_ascii=False,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return "0x" + digest


def _guardar_fallback(registro):
    ruta = Path(RUTA_FALLBACK)
    datos = []
    if ruta.exists():
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    datos.append(registro)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def _registrar_onchain(hash_hex):
    """Devuelve el tx hash. Lanza excepcion si no se puede (la captura registrar_decision)."""
    from web3 import Web3
    rpc = os.environ["RPC_URL"]
    pk = os.environ["PRIVATE_KEY"]
    address = os.environ["CONTRACT_ADDRESS"]
    if not address:
        raise RuntimeError("Sin CONTRACT_ADDRESS")
    w3 = Web3(Web3.HTTPProvider(rpc))
    cuenta = w3.eth.account.from_key(pk)
    abi = json.loads(Path(RUTA_ABI).read_text(encoding="utf-8"))
    contrato = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    hash_bytes = bytes.fromhex(hash_hex[2:])
    tx = contrato.functions.registrar(hash_bytes).build_transaction({
        "from": cuenta.address,
        "nonce": w3.eth.get_transaction_count(cuenta.address),
        "gas": 120000,
        "gasPrice": w3.eth.gas_price,
    })
    firmada = cuenta.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(firmada.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    return tx_hash.hex()


def registrar_decision(postulante, texto_regla, resultado):
    h = calcular_hash(postulante, texto_regla, resultado)
    try:
        tx_hash = _registrar_onchain(h)
        registro = {"hash": h, "tx": tx_hash, "modo": "onchain", "timestamp": time.time()}
    except Exception as e:
        registro = {"hash": h, "tx": None, "modo": "fallback",
                    "error": str(e), "timestamp": time.time()}
        _guardar_fallback(registro)
    return registro
