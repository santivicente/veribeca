import os
import json
from contracts.web3_client import registrar_decision, calcular_hash


def test_calcular_hash_determinista():
    h1 = calcular_hash({"id": 1}, "regla X", True)
    h2 = calcular_hash({"id": 1}, "regla X", True)
    assert h1 == h2 and h1.startswith("0x") and len(h1) == 66


def test_fallback_cuando_no_hay_config(tmp_path, monkeypatch):
    ledger = tmp_path / "fallback_ledger.json"
    monkeypatch.setenv("CONTRACT_ADDRESS", "")
    monkeypatch.setattr("contracts.web3_client.RUTA_FALLBACK", str(ledger))
    resultado = registrar_decision({"id": 7}, "regla Y", False)
    assert resultado["modo"] == "fallback"
    assert resultado["hash"].startswith("0x")
    datos = json.loads(ledger.read_text(encoding="utf-8"))
    assert any(r["hash"] == resultado["hash"] for r in datos)
