from dsl.tokens import TipoToken
from dsl.ast_nodes import Regla, Comparacion, OpBinaria, Negacion
from dsl.errors import ErrorSintactico

OPS_COMP = {
    TipoToken.LT: "<", TipoToken.LE: "<=", TipoToken.GT: ">",
    TipoToken.GE: ">=", TipoToken.EQ: "==", TipoToken.NE: "!=",
}


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def actual(self):
        return self.tokens[self.i]

    def consumir(self, tipo):
        tok = self.actual()
        if tok.tipo != tipo:
            raise ErrorSintactico(f"Se esperaba {tipo.name} pero se encontro {tok.tipo.name} en posicion {tok.pos}")
        self.i += 1
        return tok

    def parsear_regla(self):
        self.consumir(TipoToken.SI)
        cond = self.expr()
        self.consumir(TipoToken.ENTONCES)
        self.consumir(TipoToken.ELEGIBLE)
        self.consumir(TipoToken.EOF)
        return Regla(cond)

    def expr(self):
        nodo = self.term()
        while self.actual().tipo == TipoToken.O:
            self.consumir(TipoToken.O)
            nodo = OpBinaria("O", nodo, self.term())
        return nodo

    def term(self):
        nodo = self.factor()
        while self.actual().tipo == TipoToken.Y:
            self.consumir(TipoToken.Y)
            nodo = OpBinaria("Y", nodo, self.factor())
        return nodo

    def factor(self):
        tok = self.actual()
        if tok.tipo == TipoToken.NO:
            self.consumir(TipoToken.NO)
            return Negacion(self.factor())
        if tok.tipo == TipoToken.LPAREN:
            self.consumir(TipoToken.LPAREN)
            nodo = self.expr()
            self.consumir(TipoToken.RPAREN)
            return nodo
        return self.comparacion()

    def comparacion(self):
        ident = self.consumir(TipoToken.IDENT)
        op_tok = self.actual()
        if op_tok.tipo not in OPS_COMP:
            raise ErrorSintactico(f"Se esperaba un operador de comparacion en posicion {op_tok.pos}")
        self.i += 1
        valor_tok = self.actual()
        if valor_tok.tipo not in (TipoToken.NUMERO, TipoToken.TEXTO, TipoToken.BOOL):
            raise ErrorSintactico(f"Se esperaba un valor en posicion {valor_tok.pos}")
        self.i += 1
        return Comparacion(ident.valor, OPS_COMP[op_tok.tipo], valor_tok.valor)


def parsear(tokens):
    return _Parser(tokens).parsear_regla()
