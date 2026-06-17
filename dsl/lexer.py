from dsl.tokens import Token, TipoToken
from dsl.errors import ErrorLexico

PALABRAS_CLAVE = {
    "SI": TipoToken.SI,
    "ENTONCES": TipoToken.ENTONCES,
    "elegible": TipoToken.ELEGIBLE,
    "Y": TipoToken.Y,
    "O": TipoToken.O,
    "NO": TipoToken.NO,
    "verdadero": TipoToken.BOOL,
    "falso": TipoToken.BOOL,
}


def tokenizar(texto):
    tokens = []
    i = 0
    n = len(texto)
    while i < n:
        c = texto[i]
        if c.isspace():
            i += 1
            continue
        if c == "(":
            tokens.append(Token(TipoToken.LPAREN, "(", i)); i += 1; continue
        if c == ")":
            tokens.append(Token(TipoToken.RPAREN, ")", i)); i += 1; continue
        if c == "<":
            if i + 1 < n and texto[i + 1] == "=":
                tokens.append(Token(TipoToken.LE, "<=", i)); i += 2
            else:
                tokens.append(Token(TipoToken.LT, "<", i)); i += 1
            continue
        if c == ">":
            if i + 1 < n and texto[i + 1] == "=":
                tokens.append(Token(TipoToken.GE, ">=", i)); i += 2
            else:
                tokens.append(Token(TipoToken.GT, ">", i)); i += 1
            continue
        if c == "=" and i + 1 < n and texto[i + 1] == "=":
            tokens.append(Token(TipoToken.EQ, "==", i)); i += 2; continue
        if c == "!" and i + 1 < n and texto[i + 1] == "=":
            tokens.append(Token(TipoToken.NE, "!=", i)); i += 2; continue
        if c == '"':
            j = i + 1
            while j < n and texto[j] != '"':
                j += 1
            if j >= n:
                raise ErrorLexico(f"Cadena sin cerrar en posicion {i}")
            tokens.append(Token(TipoToken.TEXTO, texto[i + 1:j], i)); i = j + 1; continue
        if c.isdigit():
            j = i
            while j < n and (texto[j].isdigit() or texto[j] == "."):
                j += 1
            num_txt = texto[i:j]
            num = float(num_txt) if "." in num_txt else int(num_txt)
            tokens.append(Token(TipoToken.NUMERO, num, i)); i = j; continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (texto[j].isalnum() or texto[j] == "_"):
                j += 1
            palabra = texto[i:j]
            if palabra in PALABRAS_CLAVE:
                tipo = PALABRAS_CLAVE[palabra]
                if tipo == TipoToken.BOOL:
                    tokens.append(Token(tipo, palabra == "verdadero", i))
                else:
                    tokens.append(Token(tipo, palabra, i))
            else:
                tokens.append(Token(TipoToken.IDENT, palabra, i))
            i = j; continue
        raise ErrorLexico(f"Caracter inesperado '{c}' en posicion {i}")
    tokens.append(Token(TipoToken.EOF, None, n))
    return tokens
