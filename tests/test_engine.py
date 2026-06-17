import pytest
from dsl.engine import compilar_regla, MotorReglas
from dsl.errors import ErrorDeTipos

SCHEMA = {"ingreso": "numero", "promedio": "numero"}


def test_compilar_y_evaluar():
    motor = compilar_regla("SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible", SCHEMA)
    assert isinstance(motor, MotorReglas)
    assert motor.evaluar({"ingreso": 200000, "promedio": 9}) is True
    assert motor.evaluar({"ingreso": 400000, "promedio": 9}) is False


def test_compilar_regla_invalida_falla_temprano():
    with pytest.raises(ErrorDeTipos):
        compilar_regla("SI inexistente < 5 ENTONCES elegible", SCHEMA)
