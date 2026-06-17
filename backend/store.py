"""Almacenamiento simple en memoria para el MVP (sin base de datos)."""

_estado = {"motor": None, "texto_regla": None, "postulantes": []}


def set_motor(motor, texto):
    _estado["motor"] = motor
    _estado["texto_regla"] = texto


def get_motor():
    return _estado["motor"], _estado["texto_regla"]


def set_postulantes(lista):
    _estado["postulantes"] = lista


def get_postulantes():
    return _estado["postulantes"]
