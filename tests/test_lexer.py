import pytest
from dsl.lexer import tokenizar
from dsl.tokens import TipoToken
from dsl.errors import ErrorLexico


def test_tokeniza_comparacion_simple():
    tokens = tokenizar("ingreso < 300000")
    tipos = [t.tipo for t in tokens]
    assert tipos == [TipoToken.IDENT, TipoToken.LT, TipoToken.NUMERO, TipoToken.EOF]
    assert tokens[0].valor == "ingreso"
    assert tokens[2].valor == 300000


def test_tokeniza_regla_completa():
    tokens = tokenizar('SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible')
    tipos = [t.tipo for t in tokens]
    assert tipos == [
        TipoToken.SI, TipoToken.IDENT, TipoToken.LT, TipoToken.NUMERO,
        TipoToken.Y, TipoToken.IDENT, TipoToken.GE, TipoToken.NUMERO,
        TipoToken.ENTONCES, TipoToken.ELEGIBLE, TipoToken.EOF,
    ]


def test_tokeniza_texto_y_bool():
    tokens = tokenizar('carrera == "ingenieria" Y trabaja == verdadero')
    assert tokens[2].tipo == TipoToken.TEXTO and tokens[2].valor == "ingenieria"
    assert tokens[6].tipo == TipoToken.BOOL and tokens[6].valor is True


def test_caracter_invalido_lanza_error():
    with pytest.raises(ErrorLexico):
        tokenizar("ingreso @ 5")
