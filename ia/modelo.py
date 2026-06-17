import numpy as np

RANGOS = {
    "ingreso_familiar": (50000, 600000),
    "integrantes_familia": (1, 8),
    "distancia_km": (0, 120),
}
PESOS = {"ingreso_familiar": 0.5, "integrantes_familia": 0.3, "distancia_km": 0.2}


def _norm(valor, lo, hi):
    return max(0.0, min(1.0, (valor - lo) / (hi - lo)))


def calcular_score(postulante):
    lo, hi = RANGOS["ingreso_familiar"]
    s_ingreso = 1.0 - _norm(postulante["ingreso_familiar"], lo, hi)
    lo, hi = RANGOS["integrantes_familia"]
    s_integrantes = _norm(postulante["integrantes_familia"], lo, hi)
    lo, hi = RANGOS["distancia_km"]
    s_distancia = _norm(postulante["distancia_km"], lo, hi)
    score = (
        PESOS["ingreso_familiar"] * s_ingreso
        + PESOS["integrantes_familia"] * s_integrantes
        + PESOS["distancia_km"] * s_distancia
    )
    return round(float(score), 4)


def priorizar(postulantes):
    con_score = [{**p, "score": calcular_score(p)} for p in postulantes]
    return sorted(con_score, key=lambda p: p["score"], reverse=True)


def entrenar_modelo(filas):
    """Demostracion del uso de scikit-learn: aprende a reproducir el score con regresion lineal.
    Devuelve el modelo entrenado y el R^2; sirve para la memoria tecnica."""
    from sklearn.linear_model import LinearRegression
    X = np.array([[f["ingreso_familiar"], f["integrantes_familia"], f["distancia_km"]] for f in filas])
    y = np.array([calcular_score(f) for f in filas])
    modelo = LinearRegression().fit(X, y)
    return modelo, modelo.score(X, y)
