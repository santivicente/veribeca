from fastapi import FastAPI, HTTPException
from backend.schemas import ReglaIn, PostulantesIn
from backend import store
from dsl.engine import compilar_regla
from dsl.errors import ErrorDSL
from ia.modelo import priorizar
from contracts.web3_client import registrar_decision

app = FastAPI(title="VeriBeca API")


@app.post("/reglas")
def cargar_reglas(body: ReglaIn):
    try:
        motor = compilar_regla(body.texto, body.schema_vars)
    except ErrorDSL as e:
        raise HTTPException(status_code=400, detail=str(e))
    store.set_motor(motor, body.texto)
    return {"ok": True, "mensaje": "Regla valida y cargada"}


@app.post("/postulantes")
def cargar_postulantes(body: PostulantesIn):
    store.set_postulantes(body.postulantes)
    return {"ok": True, "cantidad": len(body.postulantes)}


@app.post("/evaluar")
def evaluar():
    motor, texto = store.get_motor()
    if motor is None:
        raise HTTPException(status_code=400, detail="No hay regla cargada")
    postulantes = store.get_postulantes()
    elegibles, no_elegibles = [], []
    for p in postulantes:
        if motor.evaluar(p):
            elegibles.append(p)
        else:
            no_elegibles.append(p)
    ranking = priorizar(elegibles)
    # Registra on-chain solo al #1 (el de mayor prioridad); el resto en modo rápido (fallback).
    for i, p in enumerate(ranking):
        cert = registrar_decision(p, texto, True, forzar_fallback=(i != 0))
        p["certificado"] = cert
    return {"ranking": ranking, "no_elegibles": no_elegibles}
