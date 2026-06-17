import pytest
from dsl.lexer import tokenizar
from dsl.parser import parsear
from dsl.types import chequear_tipos
from dsl.errors import ErrorDeTipos

SCHEMA = {
    "ingreso": "numero",
    "promedio": "numero",
    "trabaja": "booleano",
    "carrera": "texto",
}


def test_regla_valida_pasa():
    arbol = parsear(tokenizar("SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible"))
    chequear_tipos(arbol, SCHEMA)


def test_variable_inexistente():
    arbol = parsear(tokenizar("SI inexistente < 5 ENTONCES elegible"))
    with pytest.raises(ErrorDeTipos):
        chequear_tipos(arbol, SCHEMA)


def test_comparar_texto_con_numero():
    arbol = parsear(tokenizar("SI carrera < 5 ENTONCES elegible"))
    with pytest.raises(ErrorDeTipos):
        chequear_tipos(arbol, SCHEMA)


def test_relacional_sobre_booleano():
    arbol = parsear(tokenizar("SI trabaja > 1 ENTONCES elegible"))
    with pytest.raises(ErrorDeTipos):
        chequear_tipos(arbol, SCHEMA)


def test_igualdad_texto_valida():
    arbol = parsear(tokenizar('SI carrera == "ingenieria" ENTONCES elegible'))
    chequear_tipos(arbol, SCHEMA)
