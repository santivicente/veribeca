from dsl.lexer import tokenizar
from dsl.parser import parsear
from dsl.interpreter import evaluar


def _arbol(texto):
    return parsear(tokenizar(texto))


def test_evalua_elegible_true():
    arbol = _arbol("SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible")
    assert evaluar(arbol, {"ingreso": 250000, "promedio": 8}) is True


def test_evalua_elegible_false():
    arbol = _arbol("SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible")
    assert evaluar(arbol, {"ingreso": 250000, "promedio": 6}) is False


def test_evalua_o_y_negacion():
    arbol = _arbol("SI NO trabaja == verdadero O ingreso < 100000 ENTONCES elegible")
    assert evaluar(arbol, {"trabaja": False, "ingreso": 999999}) is True
    assert evaluar(arbol, {"trabaja": True, "ingreso": 999999}) is False


def test_evalua_texto():
    arbol = _arbol('SI carrera == "medicina" ENTONCES elegible')
    assert evaluar(arbol, {"carrera": "medicina"}) is True
    assert evaluar(arbol, {"carrera": "derecho"}) is False
