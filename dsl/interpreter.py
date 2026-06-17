from dsl.ast_nodes import Regla, Comparacion, OpBinaria, Negacion
from dsl.errors import ErrorDSL

import operator

OPERADORES = {
    "<": operator.lt, "<=": operator.le, ">": operator.gt,
    ">=": operator.ge, "==": operator.eq, "!=": operator.ne,
}


def _eval_nodo(nodo, registro):
    if isinstance(nodo, Comparacion):
        if nodo.variable not in registro:
            raise ErrorDSL(f"El postulante no tiene el dato '{nodo.variable}'")
        return OPERADORES[nodo.operador](registro[nodo.variable], nodo.valor)
    if isinstance(nodo, OpBinaria):
        izq = _eval_nodo(nodo.izquierda, registro)
        der = _eval_nodo(nodo.derecha, registro)
        return (izq and der) if nodo.operador == "Y" else (izq or der)
    if isinstance(nodo, Negacion):
        return not _eval_nodo(nodo.expr, registro)
    raise ErrorDSL(f"Nodo desconocido: {nodo!r}")


def evaluar(regla, registro):
    return bool(_eval_nodo(regla.condicion, registro))
