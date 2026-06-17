import pytest
from dsl.lexer import tokenizar
from dsl.parser import parsear
from dsl.ast_nodes import Regla, Comparacion, OpBinaria, Negacion
from dsl.errors import ErrorSintactico


def test_parsea_comparacion_simple():
    arbol = parsear(tokenizar("SI ingreso < 300000 ENTONCES elegible"))
    assert isinstance(arbol, Regla)
    assert isinstance(arbol.condicion, Comparacion)
    assert arbol.condicion.variable == "ingreso"
    assert arbol.condicion.operador == "<"
    assert arbol.condicion.valor == 300000


def test_precedencia_y_sobre_o():
    arbol = parsear(tokenizar("SI a > 1 O b > 2 Y c > 3 ENTONCES elegible"))
    assert isinstance(arbol.condicion, OpBinaria)
    assert arbol.condicion.operador == "O"
    assert isinstance(arbol.condicion.derecha, OpBinaria)
    assert arbol.condicion.derecha.operador == "Y"


def test_parentesis_cambian_precedencia():
    arbol = parsear(tokenizar("SI (a > 1 O b > 2) Y c > 3 ENTONCES elegible"))
    assert arbol.condicion.operador == "Y"
    assert arbol.condicion.izquierda.operador == "O"


def test_negacion():
    arbol = parsear(tokenizar("SI NO trabaja == verdadero ENTONCES elegible"))
    assert isinstance(arbol.condicion, Negacion)


def test_falta_entonces_lanza_error():
    with pytest.raises(ErrorSintactico):
        parsear(tokenizar("SI a > 1 elegible"))
