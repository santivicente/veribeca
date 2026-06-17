from dsl.lexer import tokenizar
from dsl.parser import parsear
from dsl.types import chequear_tipos
from dsl.interpreter import evaluar


class MotorReglas:
    def __init__(self, regla, schema, texto):
        self._regla = regla
        self._schema = schema
        self.texto = texto

    def evaluar(self, registro):
        return evaluar(self._regla, registro)


def compilar_regla(texto, schema):
    """Pipeline completo: lexer -> parser -> type-checker. Lanza ErrorDSL si algo falla."""
    tokens = tokenizar(texto)
    arbol = parsear(tokens)
    chequear_tipos(arbol, schema)
    return MotorReglas(arbol, schema, texto)
