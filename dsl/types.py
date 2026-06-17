from dsl.ast_nodes import Regla, Comparacion, OpBinaria, Negacion
from dsl.errors import ErrorDeTipos

RELACIONALES = {"<", "<=", ">", ">="}
IGUALDAD = {"==", "!="}


def _tipo_valor(valor):
    if isinstance(valor, bool):
        return "booleano"
    if isinstance(valor, (int, float)):
        return "numero"
    if isinstance(valor, str):
        return "texto"
    raise ErrorDeTipos(f"Valor de tipo desconocido: {valor!r}")


def _chequear_nodo(nodo, schema):
    if isinstance(nodo, Comparacion):
        if nodo.variable not in schema:
            raise ErrorDeTipos(f"Variable inexistente: '{nodo.variable}'")
        tipo_var = schema[nodo.variable]
        tipo_val = _tipo_valor(nodo.valor)
        if tipo_var != tipo_val:
            raise ErrorDeTipos(
                f"No se puede comparar '{nodo.variable}' ({tipo_var}) con un {tipo_val}"
            )
        if nodo.operador in RELACIONALES and tipo_var != "numero":
            raise ErrorDeTipos(
                f"El operador '{nodo.operador}' solo aplica a numeros, no a {tipo_var}"
            )
        return
    if isinstance(nodo, OpBinaria):
        _chequear_nodo(nodo.izquierda, schema)
        _chequear_nodo(nodo.derecha, schema)
        return
    if isinstance(nodo, Negacion):
        _chequear_nodo(nodo.expr, schema)
        return
    raise ErrorDeTipos(f"Nodo desconocido en el AST: {nodo!r}")


def chequear_tipos(regla, schema):
    if not isinstance(regla, Regla):
        raise ErrorDeTipos("Se esperaba una Regla en la raiz del AST")
    _chequear_nodo(regla.condicion, schema)
