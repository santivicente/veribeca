# VeriBeca — Plan de Implementación

> Plan de implementación dividido en tareas. Cada paso usa checkboxes (`- [ ]`) para hacer seguimiento del avance del equipo.

**Goal:** Construir un MVP demostrable de VeriBeca: un DSL tipado para reglas de elegibilidad de becas, con backend, IA de priorización, registro en blockchain (testnet) y UI, más toda la documentación de la hackathon.

**Architecture:** Monorepo Python. El núcleo es un motor DSL (lexer → parser → type-checker → intérprete) como paquete puro y testeado. Un backend FastAPI orquesta DSL + IA (scikit-learn) + registro de hash on-chain (Polygon Amoy con fallback local). Una UI Streamlit consume el backend. Documentación en `docs/`.

**Tech Stack:** Python 3.x, pytest, FastAPI, Uvicorn, scikit-learn, pandas, web3.py, Solidity, Streamlit.

---

## Cómo paralelizar (3 personas, meta ~5 días)

- **Fase 0 (juntos, ~1h):** Tareas 1-2 (setup de repo). Una persona lo hace y pushea; las otras clonan.
- **Día 1-2 en paralelo:**
  - **Dev A:** Tareas 3-10 (DSL completo — es el núcleo y bloquea al backend).
  - **Dev B:** Tareas 11-13 (dataset sintético + IA).
  - **Dev C:** Tareas 14-16 (smart contract + cliente web3 + fallback).
- **Día 3:** Tarea 17-19 (backend, integra DSL+IA+web3). Lo hace Dev A apenas termina el DSL; B y C ya entregaron sus módulos.
- **Día 4:** Tareas 20-21 (frontend Streamlit + evidencias). 
- **Día 5:** Tareas 22-27 (documentación + video + pulido).

Los módulos de B y C no dependen entre sí ni del DSL, por eso van en paralelo desde el día 1.

---

## File Structure

```
veribeca/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ dsl/
│  ├─ __init__.py
│  ├─ tokens.py         # definición de tipos de token
│  ├─ lexer.py          # texto → tokens
│  ├─ ast_nodes.py      # nodos del AST
│  ├─ parser.py         # tokens → AST
│  ├─ types.py          # type-checker
│  ├─ interpreter.py    # evalúa AST sobre un postulante
│  ├─ errors.py         # excepciones del DSL
│  └─ engine.py         # fachada: valida + evalúa
├─ tests/
│  ├─ test_lexer.py
│  ├─ test_parser.py
│  ├─ test_types.py
│  ├─ test_interpreter.py
│  └─ test_engine.py
├─ ia/
│  ├─ __init__.py
│  ├─ generar_dataset.py
│  ├─ modelo.py
│  └─ tests/test_modelo.py
├─ contracts/
│  ├─ AuditoriaBecas.sol
│  ├─ deploy.py
│  ├─ web3_client.py
│  └─ fallback_ledger.json   # generado en runtime (ignorado por git salvo ejemplo)
├─ backend/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ schemas.py
│  └─ store.py
├─ frontend/
│  └─ app.py
├─ data/
│  ├─ reglas_ejemplo.txt
│  └─ postulantes.csv     # generado por ia/generar_dataset.py
└─ docs/
   ├─ lean-canvas.md
   ├─ memoria-tecnica.md
   ├─ pitch-deck.md
   ├─ guion-video.md
   └─ evidencias/
```

## Definición de la gramática del DSL (referencia para todas las tareas)

```
regla       := "SI" expr "ENTONCES" "elegible"
expr        := term ("O" term)*
term        := factor ("Y" factor)*
factor      := "NO" factor | "(" expr ")" | comparacion
comparacion := IDENT op valor
op          := "<" | "<=" | ">" | ">=" | "==" | "!="
valor       := NUMBER | STRING | BOOL
```

**Schema de variables:** diccionario `{nombre: tipo}` con tipo en `{"numero", "booleano", "texto"}`.
Ejemplo de schema de un postulante:
`{"ingreso_familiar": "numero", "promedio": "numero", "integrantes_familia": "numero", "distancia_km": "numero", "trabaja": "booleano", "carrera": "texto"}`

**Reglas de tipos:**
- La variable de la izquierda debe existir en el schema.
- Operadores relacionales (`<`, `<=`, `>`, `>=`) solo se permiten sobre `numero`.
- `==` y `!=` se permiten sobre cualquier tipo, pero el tipo del valor debe coincidir con el de la variable.
- `Y`, `O`, `NO` operan sobre booleanos (resultado de comparaciones).

**Regla de ejemplo válida:**
`SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`

---

## Task 1: Inicializar repositorio y estructura

**Files:**
- Create: `requirements.txt`, `.gitignore`, `.env.example`, `dsl/__init__.py`, `ia/__init__.py`, `backend/__init__.py`, `tests/__init__.py`

- [ ] **Step 1: Crear `requirements.txt`**

```
fastapi
uvicorn[standard]
pydantic
scikit-learn
pandas
numpy
web3
python-dotenv
streamlit
requests
pytest
```

- [ ] **Step 2: Crear `.gitignore`**

```
__pycache__/
*.pyc
.venv/
venv/
.env
contracts/fallback_ledger.json
.pytest_cache/
*.egg-info/
```

- [ ] **Step 3: Crear `.env.example`**

```
AMOY_RPC_URL=https://rpc-amoy.polygon.technology
PRIVATE_KEY=tu_clave_privada_de_testnet_aqui
CONTRACT_ADDRESS=
```

- [ ] **Step 4: Crear paquetes vacíos**

Crear archivos vacíos: `dsl/__init__.py`, `ia/__init__.py`, `backend/__init__.py`, `tests/__init__.py`.

- [ ] **Step 5: Crear y activar entorno e instalar**

Run (Windows PowerShell):
```
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```
Expected: instala sin errores.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: estructura inicial del repo y dependencias"
```

---

## Task 2: Definir tipos de token y excepciones del DSL

**Files:**
- Create: `dsl/tokens.py`, `dsl/errors.py`

- [ ] **Step 1: Crear `dsl/tokens.py`**

```python
from dataclasses import dataclass
from enum import Enum, auto


class TipoToken(Enum):
    SI = auto()
    ENTONCES = auto()
    ELEGIBLE = auto()
    Y = auto()
    O = auto()
    NO = auto()
    IDENT = auto()
    NUMERO = auto()
    TEXTO = auto()
    BOOL = auto()
    LT = auto()    # <
    LE = auto()    # <=
    GT = auto()    # >
    GE = auto()    # >=
    EQ = auto()    # ==
    NE = auto()    # !=
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass
class Token:
    tipo: TipoToken
    valor: object
    pos: int
```

- [ ] **Step 2: Crear `dsl/errors.py`**

```python
class ErrorDSL(Exception):
    """Error base del DSL."""


class ErrorLexico(ErrorDSL):
    pass


class ErrorSintactico(ErrorDSL):
    pass


class ErrorDeTipos(ErrorDSL):
    pass
```

- [ ] **Step 3: Commit**

```bash
git add dsl/tokens.py dsl/errors.py
git commit -m "feat(dsl): tipos de token y excepciones"
```

---

## Task 3: Lexer — tokens básicos

**Files:**
- Create: `dsl/lexer.py`
- Test: `tests/test_lexer.py`

- [ ] **Step 1: Escribir el test que falla**

```python
from dsl.lexer import tokenizar
from dsl.tokens import TipoToken


def test_tokeniza_comparacion_simple():
    tokens = tokenizar("ingreso < 300000")
    tipos = [t.tipo for t in tokens]
    assert tipos == [TipoToken.IDENT, TipoToken.LT, TipoToken.NUMERO, TipoToken.EOF]
    assert tokens[0].valor == "ingreso"
    assert tokens[2].valor == 300000
```

- [ ] **Step 2: Correr el test y verificar que falla**

Run: `pytest tests/test_lexer.py::test_tokeniza_comparacion_simple -v`
Expected: FAIL — `ModuleNotFoundError` o `cannot import name 'tokenizar'`.

- [ ] **Step 3: Implementar `dsl/lexer.py`**

```python
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
                raise ErrorLexico(f"Cadena sin cerrar en posición {i}")
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
        raise ErrorLexico(f"Carácter inesperado '{c}' en posición {i}")
    tokens.append(Token(TipoToken.EOF, None, n))
    return tokens
```

- [ ] **Step 4: Correr el test y verificar que pasa**

Run: `pytest tests/test_lexer.py::test_tokeniza_comparacion_simple -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dsl/lexer.py tests/test_lexer.py
git commit -m "feat(dsl): lexer con comparaciones, números e identificadores"
```

---

## Task 4: Lexer — palabras clave, texto y booleanos

**Files:**
- Test: `tests/test_lexer.py`

- [ ] **Step 1: Agregar tests que fallan**

```python
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
    import pytest
    from dsl.errors import ErrorLexico
    with pytest.raises(ErrorLexico):
        tokenizar("ingreso @ 5")
```

- [ ] **Step 2: Correr y verificar que pasan**

Run: `pytest tests/test_lexer.py -v`
Expected: PASS (el lexer de la Tarea 3 ya cubre estos casos).

- [ ] **Step 3: Commit**

```bash
git add tests/test_lexer.py
git commit -m "test(dsl): cobertura de palabras clave, texto, bool y errores léxicos"
```

---

## Task 5: AST y parser — comparaciones

**Files:**
- Create: `dsl/ast_nodes.py`, `dsl/parser.py`
- Test: `tests/test_parser.py`

- [ ] **Step 1: Crear `dsl/ast_nodes.py`**

```python
from dataclasses import dataclass


@dataclass
class Comparacion:
    variable: str
    operador: str   # uno de: < <= > >= == !=
    valor: object


@dataclass
class OpBinaria:
    operador: str   # "Y" u "O"
    izquierda: object
    derecha: object


@dataclass
class Negacion:
    expr: object


@dataclass
class Regla:
    condicion: object   # raíz de la expresión booleana
```

- [ ] **Step 2: Escribir el test que falla**

```python
from dsl.lexer import tokenizar
from dsl.parser import parsear
from dsl.ast_nodes import Regla, Comparacion


def test_parsea_comparacion_simple():
    arbol = parsear(tokenizar("SI ingreso < 300000 ENTONCES elegible"))
    assert isinstance(arbol, Regla)
    assert isinstance(arbol.condicion, Comparacion)
    assert arbol.condicion.variable == "ingreso"
    assert arbol.condicion.operador == "<"
    assert arbol.condicion.valor == 300000
```

- [ ] **Step 3: Correr y verificar que falla**

Run: `pytest tests/test_parser.py::test_parsea_comparacion_simple -v`
Expected: FAIL — `cannot import name 'parsear'`.

- [ ] **Step 4: Implementar `dsl/parser.py`**

```python
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
            raise ErrorSintactico(f"Se esperaba {tipo.name} pero se encontró {tok.tipo.name} en posición {tok.pos}")
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
            raise ErrorSintactico(f"Se esperaba un operador de comparación en posición {op_tok.pos}")
        self.i += 1
        valor_tok = self.actual()
        if valor_tok.tipo not in (TipoToken.NUMERO, TipoToken.TEXTO, TipoToken.BOOL):
            raise ErrorSintactico(f"Se esperaba un valor en posición {valor_tok.pos}")
        self.i += 1
        return Comparacion(ident.valor, OPS_COMP[op_tok.tipo], valor_tok.valor)


def parsear(tokens):
    return _Parser(tokens).parsear_regla()
```

- [ ] **Step 5: Correr y verificar que pasa**

Run: `pytest tests/test_parser.py::test_parsea_comparacion_simple -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add dsl/ast_nodes.py dsl/parser.py tests/test_parser.py
git commit -m "feat(dsl): AST y parser de comparaciones"
```

---

## Task 6: Parser — precedencia Y/O, NO y paréntesis

**Files:**
- Test: `tests/test_parser.py`

- [ ] **Step 1: Agregar tests que fallan**

```python
from dsl.ast_nodes import OpBinaria, Negacion


def test_precedencia_y_sobre_o():
    arbol = parsear(tokenizar("SI a > 1 O b > 2 Y c > 3 ENTONCES elegible"))
    # debe agruparse como: a>1 O (b>2 Y c>3)
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
    import pytest
    from dsl.errors import ErrorSintactico
    with pytest.raises(ErrorSintactico):
        parsear(tokenizar("SI a > 1 elegible"))
```

- [ ] **Step 2: Correr y verificar que pasan**

Run: `pytest tests/test_parser.py -v`
Expected: PASS (el parser de la Tarea 5 ya implementa precedencia y errores).

- [ ] **Step 3: Commit**

```bash
git add tests/test_parser.py
git commit -m "test(dsl): precedencia, paréntesis, negación y errores sintácticos"
```

---

## Task 7: Type-checker

**Files:**
- Create: `dsl/types.py`
- Test: `tests/test_types.py`

- [ ] **Step 1: Escribir los tests que fallan**

```python
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
    chequear_tipos(arbol, SCHEMA)  # no lanza


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
    chequear_tipos(arbol, SCHEMA)  # no lanza
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `pytest tests/test_types.py -v`
Expected: FAIL — `cannot import name 'chequear_tipos'`.

- [ ] **Step 3: Implementar `dsl/types.py`**

```python
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
                f"El operador '{nodo.operador}' solo aplica a números, no a {tipo_var}"
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
        raise ErrorDeTipos("Se esperaba una Regla en la raíz del AST")
    _chequear_nodo(regla.condicion, schema)
```

- [ ] **Step 4: Correr y verificar que pasan**

Run: `pytest tests/test_types.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dsl/types.py tests/test_types.py
git commit -m "feat(dsl): type-checker del DSL"
```

---

## Task 8: Intérprete

**Files:**
- Create: `dsl/interpreter.py`
- Test: `tests/test_interpreter.py`

- [ ] **Step 1: Escribir los tests que fallan**

```python
from dsl.lexer import tokenizar
from dsl.parser import parsear
from dsl.interpreter import evaluar


def _arbol(texto):
    return parsear(tokenizar(texto))


def test_evalua_elegible_true():
    arbol = _arbol("SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible")
    registro = {"ingreso": 250000, "promedio": 8}
    assert evaluar(arbol, registro) is True


def test_evalua_elegible_false():
    arbol = _arbol("SI ingreso < 300000 Y promedio >= 7 ENTONCES elegible")
    registro = {"ingreso": 250000, "promedio": 6}
    assert evaluar(arbol, registro) is False


def test_evalua_o_y_negacion():
    arbol = _arbol("SI NO trabaja == verdadero O ingreso < 100000 ENTONCES elegible")
    assert evaluar(arbol, {"trabaja": False, "ingreso": 999999}) is True
    assert evaluar(arbol, {"trabaja": True, "ingreso": 999999}) is False


def test_evalua_texto():
    arbol = _arbol('SI carrera == "medicina" ENTONCES elegible')
    assert evaluar(arbol, {"carrera": "medicina"}) is True
    assert evaluar(arbol, {"carrera": "derecho"}) is False
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `pytest tests/test_interpreter.py -v`
Expected: FAIL — `cannot import name 'evaluar'`.

- [ ] **Step 3: Implementar `dsl/interpreter.py`**

```python
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
```

- [ ] **Step 4: Correr y verificar que pasan**

Run: `pytest tests/test_interpreter.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dsl/interpreter.py tests/test_interpreter.py
git commit -m "feat(dsl): intérprete que evalúa reglas sobre postulantes"
```

---

## Task 9: Fachada del motor (`engine`)

**Files:**
- Create: `dsl/engine.py`
- Test: `tests/test_engine.py`

- [ ] **Step 1: Escribir los tests que fallan**

```python
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
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `pytest tests/test_engine.py -v`
Expected: FAIL — `cannot import name 'compilar_regla'`.

- [ ] **Step 3: Implementar `dsl/engine.py`**

```python
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
```

- [ ] **Step 4: Correr y verificar que pasan**

Run: `pytest tests/test_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dsl/engine.py tests/test_engine.py
git commit -m "feat(dsl): fachada compilar_regla + MotorReglas"
```

---

## Task 10: Reglas de ejemplo y suite completa

**Files:**
- Create: `data/reglas_ejemplo.txt`

- [ ] **Step 1: Crear `data/reglas_ejemplo.txt`**

```
SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible
SI ingreso_familiar < 150000 ENTONCES elegible
SI promedio >= 8 Y integrantes_familia >= 4 ENTONCES elegible
SI (ingreso_familiar < 200000 O distancia_km > 50) Y promedio >= 6 ENTONCES elegible
SI NO trabaja == verdadero Y ingreso_familiar < 250000 ENTONCES elegible
SI carrera == "medicina" Y promedio >= 7 ENTONCES elegible
```

- [ ] **Step 2: Correr toda la suite del DSL**

Run: `pytest tests/ -v`
Expected: PASS — todos los tests del DSL en verde.

- [ ] **Step 3: Commit**

```bash
git add data/reglas_ejemplo.txt
git commit -m "docs(dsl): reglas de ejemplo y verificación de suite completa"
```

---

## Task 11: Generador de dataset sintético

**Files:**
- Create: `ia/generar_dataset.py`
- Test: `ia/tests/test_modelo.py` (parcial)

- [ ] **Step 1: Implementar `ia/generar_dataset.py`**

```python
import csv
import random
from pathlib import Path

CARRERAS = ["medicina", "ingenieria", "derecho", "psicologia", "contaduria"]


def generar(n=200, semilla=42, salida="data/postulantes.csv"):
    random.seed(semilla)
    filas = []
    for i in range(1, n + 1):
        ingreso = random.randint(50000, 600000)
        promedio = round(random.uniform(4, 10), 1)
        integrantes = random.randint(1, 8)
        distancia = random.randint(0, 120)
        trabaja = random.choice([True, False])
        carrera = random.choice(CARRERAS)
        filas.append({
            "id": i,
            "nombre": f"Postulante {i}",
            "ingreso_familiar": ingreso,
            "promedio": promedio,
            "integrantes_familia": integrantes,
            "distancia_km": distancia,
            "trabaja": str(trabaja).lower(),  # "true"/"false"
            "carrera": carrera,
        })
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    with open(salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)
    return salida


if __name__ == "__main__":
    ruta = generar()
    print(f"Dataset generado en {ruta}")
```

- [ ] **Step 2: Generar el dataset**

Run: `python ia/generar_dataset.py`
Expected: imprime `Dataset generado en data/postulantes.csv` y crea el archivo.

- [ ] **Step 3: Commit**

```bash
git add ia/generar_dataset.py data/postulantes.csv
git commit -m "feat(ia): generador de dataset sintético de postulantes"
```

---

## Task 12: Modelo de scoring de vulnerabilidad

**Files:**
- Create: `ia/modelo.py`, `ia/tests/__init__.py`
- Test: `ia/tests/test_modelo.py`

- [ ] **Step 1: Escribir el test que falla**

```python
from ia.modelo import calcular_score, priorizar


def test_score_mayor_para_mas_vulnerable():
    pobre = {"ingreso_familiar": 60000, "integrantes_familia": 7, "distancia_km": 100, "promedio": 8}
    rico = {"ingreso_familiar": 590000, "integrantes_familia": 1, "distancia_km": 2, "promedio": 8}
    assert calcular_score(pobre) > calcular_score(rico)


def test_priorizar_ordena_descendente():
    elegibles = [
        {"id": 1, "ingreso_familiar": 500000, "integrantes_familia": 1, "distancia_km": 5, "promedio": 7},
        {"id": 2, "ingreso_familiar": 70000, "integrantes_familia": 6, "distancia_km": 90, "promedio": 7},
    ]
    ordenados = priorizar(elegibles)
    assert ordenados[0]["id"] == 2
    assert "score" in ordenados[0]
```

- [ ] **Step 2: Correr y verificar que falla**

Run: `pytest ia/tests/test_modelo.py -v`
Expected: FAIL — `cannot import name 'calcular_score'`.

- [ ] **Step 3: Implementar `ia/modelo.py`**

> Nota: usamos un score interpretable (combinación lineal normalizada de indicadores de
> vulnerabilidad). Es defendible ante el jurado y no requiere entrenar con datos reales. La
> función `entrenar_modelo` opcional muestra el uso de scikit-learn para la memoria técnica.

```python
import numpy as np

# Rangos usados para normalizar (coherentes con generar_dataset.py)
RANGOS = {
    "ingreso_familiar": (50000, 600000),
    "integrantes_familia": (1, 8),
    "distancia_km": (0, 120),
}
# Pesos de cada indicador en el score de vulnerabilidad (suman 1.0)
PESOS = {"ingreso_familiar": 0.5, "integrantes_familia": 0.3, "distancia_km": 0.2}


def _norm(valor, lo, hi):
    return max(0.0, min(1.0, (valor - lo) / (hi - lo)))


def calcular_score(postulante):
    lo, hi = RANGOS["ingreso_familiar"]
    # menor ingreso => más vulnerable => invertimos
    s_ingreso = 1.0 - _norm(postulante["ingreso_familiar"], lo, hi)
    lo, hi = RANGOS["integrantes_familia"]
    s_integrantes = _norm(postulante["integrantes_familia"], lo, hi)
    lo, hi = RANGOS["distancia_km"]
    s_distancia = _norm(postulante["distancia_km"], lo, hi)
    score = (
        PESOS["ingreso_familiar"] * s_ingreso
        + PESOS["integrantes_familia"] * s_integrantes
        + PESOS["distancia_km"] * s_distancia
    )
    return round(float(score), 4)


def priorizar(postulantes):
    con_score = [{**p, "score": calcular_score(p)} for p in postulantes]
    return sorted(con_score, key=lambda p: p["score"], reverse=True)


def entrenar_modelo(filas):
    """Demostración del uso de scikit-learn: aprende a reproducir el score con regresión lineal.
    Devuelve el modelo entrenado y el R^2; sirve para la memoria técnica."""
    from sklearn.linear_model import LinearRegression
    X = np.array([[f["ingreso_familiar"], f["integrantes_familia"], f["distancia_km"]] for f in filas])
    y = np.array([calcular_score(f) for f in filas])
    modelo = LinearRegression().fit(X, y)
    return modelo, modelo.score(X, y)
```

- [ ] **Step 4: Correr y verificar que pasa**

Run: `pytest ia/tests/test_modelo.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ia/modelo.py ia/tests/
git commit -m "feat(ia): score de vulnerabilidad y priorización"
```

---

## Task 13: Validar IA con scikit-learn end-to-end

**Files:**
- Test: `ia/tests/test_modelo.py`

- [ ] **Step 1: Agregar test que falla**

```python
def test_entrenar_modelo_reproduce_score():
    from ia.generar_dataset import generar
    import csv
    generar(n=100, salida="data/postulantes.csv")
    with open("data/postulantes.csv", encoding="utf-8") as f:
        filas = []
        for row in csv.DictReader(f):
            filas.append({
                "ingreso_familiar": int(row["ingreso_familiar"]),
                "integrantes_familia": int(row["integrantes_familia"]),
                "distancia_km": int(row["distancia_km"]),
            })
    from ia.modelo import entrenar_modelo
    _, r2 = entrenar_modelo(filas)
    assert r2 > 0.99  # combinación lineal => el modelo lineal la reproduce casi perfecto
```

- [ ] **Step 2: Correr y verificar que pasa**

Run: `pytest ia/tests/test_modelo.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add ia/tests/test_modelo.py
git commit -m "test(ia): scikit-learn reproduce el score (R^2 > 0.99)"
```

---

## Task 14: Smart contract de auditoría

**Files:**
- Create: `contracts/AuditoriaBecas.sol`

- [ ] **Step 1: Crear `contracts/AuditoriaBecas.sol`**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditoriaBecas {
    event DecisionRegistrada(bytes32 indexed hashDecision, uint256 timestamp, address emisor);

    mapping(bytes32 => uint256) public registros; // hash => timestamp

    function registrar(bytes32 hashDecision) external {
        require(registros[hashDecision] == 0, "Ya registrado");
        registros[hashDecision] = block.timestamp;
        emit DecisionRegistrada(hashDecision, block.timestamp, msg.sender);
    }

    function existe(bytes32 hashDecision) external view returns (bool) {
        return registros[hashDecision] != 0;
    }
}
```

- [ ] **Step 2: Compilar con Remix o solcx (manual)**

Opción simple para la demo: pegar el contrato en https://remix.ethereum.org, compilar con
Solidity 0.8.x, conectar MetaMask a Polygon Amoy y desplegar. Guardar el **address** y el
**ABI** generados. Pegar el ABI en `contracts/abi.json` (paso siguiente).

- [ ] **Step 3: Commit**

```bash
git add contracts/AuditoriaBecas.sol
git commit -m "feat(contracts): smart contract AuditoriaBecas"
```

---

## Task 15: Cliente web3 con fallback local

**Files:**
- Create: `contracts/web3_client.py`, `contracts/abi.json`
- Test: `contracts/tests/test_web3_client.py`

- [ ] **Step 1: Crear `contracts/abi.json`**

Pegar el ABI del contrato compilado. Si aún no se desplegó, usar este ABI (coincide con el contrato):

```json
[
  {"anonymous": false, "inputs": [
    {"indexed": true, "internalType": "bytes32", "name": "hashDecision", "type": "bytes32"},
    {"indexed": false, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
    {"indexed": false, "internalType": "address", "name": "emisor", "type": "address"}],
   "name": "DecisionRegistrada", "type": "event"},
  {"inputs": [{"internalType": "bytes32", "name": "hashDecision", "type": "bytes32"}],
   "name": "registrar", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
  {"inputs": [{"internalType": "bytes32", "name": "hashDecision", "type": "bytes32"}],
   "name": "existe", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
   "stateMutability": "view", "type": "function"},
  {"inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
   "name": "registros", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
   "stateMutability": "view", "type": "function"}
]
```

- [ ] **Step 2: Escribir el test que falla (modo fallback, sin red)**

```python
import os
import json
from contracts.web3_client import registrar_decision, calcular_hash


def test_calcular_hash_determinista():
    h1 = calcular_hash({"id": 1}, "regla X", True)
    h2 = calcular_hash({"id": 1}, "regla X", True)
    assert h1 == h2 and h1.startswith("0x") and len(h1) == 66


def test_fallback_cuando_no_hay_config(tmp_path, monkeypatch):
    ledger = tmp_path / "fallback_ledger.json"
    monkeypatch.setenv("CONTRACT_ADDRESS", "")  # fuerza fallback
    monkeypatch.setattr("contracts.web3_client.RUTA_FALLBACK", str(ledger))
    resultado = registrar_decision({"id": 7}, "regla Y", False)
    assert resultado["modo"] == "fallback"
    assert resultado["hash"].startswith("0x")
    datos = json.loads(ledger.read_text(encoding="utf-8"))
    assert any(r["hash"] == resultado["hash"] for r in datos)
```

- [ ] **Step 3: Correr y verificar que falla**

Run: `pytest contracts/tests/test_web3_client.py -v`
Expected: FAIL — `No module named 'contracts.web3_client'`.

- [ ] **Step 4: Implementar `contracts/web3_client.py`**

```python
import os
import json
import hashlib
import time
from pathlib import Path

RUTA_FALLBACK = "contracts/fallback_ledger.json"
RUTA_ABI = "contracts/abi.json"


def calcular_hash(postulante, texto_regla, resultado):
    payload = json.dumps(
        {"postulante": postulante, "regla": texto_regla, "resultado": resultado},
        sort_keys=True, ensure_ascii=False,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return "0x" + digest


def _guardar_fallback(registro):
    ruta = Path(RUTA_FALLBACK)
    datos = []
    if ruta.exists():
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    datos.append(registro)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def _registrar_onchain(hash_hex):
    """Devuelve el tx hash. Lanza excepción si no se puede (la captura registrar_decision)."""
    from web3 import Web3
    rpc = os.environ["AMOY_RPC_URL"]
    pk = os.environ["PRIVATE_KEY"]
    address = os.environ["CONTRACT_ADDRESS"]
    if not address:
        raise RuntimeError("Sin CONTRACT_ADDRESS")
    w3 = Web3(Web3.HTTPProvider(rpc))
    cuenta = w3.eth.account.from_key(pk)
    abi = json.loads(Path(RUTA_ABI).read_text(encoding="utf-8"))
    contrato = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    hash_bytes = bytes.fromhex(hash_hex[2:])
    tx = contrato.functions.registrar(hash_bytes).build_transaction({
        "from": cuenta.address,
        "nonce": w3.eth.get_transaction_count(cuenta.address),
        "gas": 120000,
        "gasPrice": w3.eth.gas_price,
    })
    firmada = cuenta.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(firmada.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    return tx_hash.hex()


def registrar_decision(postulante, texto_regla, resultado):
    h = calcular_hash(postulante, texto_regla, resultado)
    try:
        tx_hash = _registrar_onchain(h)
        registro = {"hash": h, "tx": tx_hash, "modo": "onchain", "timestamp": time.time()}
    except Exception as e:  # cualquier fallo de red/config => fallback
        registro = {"hash": h, "tx": None, "modo": "fallback",
                    "error": str(e), "timestamp": time.time()}
        _guardar_fallback(registro)
    return registro
```

- [ ] **Step 5: Crear `contracts/tests/__init__.py` vacío y correr**

Run: `pytest contracts/tests/test_web3_client.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add contracts/web3_client.py contracts/abi.json contracts/tests/
git commit -m "feat(contracts): cliente web3 con registro on-chain y fallback local"
```

---

## Task 16: Desplegar el contrato y registrar una transacción real

**Files:**
- Modify: `.env` (local, no se commitea)

- [ ] **Step 1: Obtener fondos de testnet**

Crear una wallet de prueba (MetaMask), copiar su private key a `.env` (`PRIVATE_KEY`), y pedir
MATIC de prueba en un faucet de Polygon Amoy (p. ej. https://faucet.polygon.technology).

- [ ] **Step 2: Desplegar (Remix) y completar `.env`**

Desplegar `AuditoriaBecas.sol` desde Remix en Amoy. Copiar el address a `CONTRACT_ADDRESS` en `.env`.

- [ ] **Step 3: Registrar una decisión real**

Run:
```
python -c "from contracts.web3_client import registrar_decision; print(registrar_decision({'id':1},'regla demo',True))"
```
Expected: imprime `{'hash': '0x...', 'tx': '0x...', 'modo': 'onchain', ...}`.

- [ ] **Step 4: Guardar evidencia**

Copiar el link del explorer (`https://amoy.polygonscan.com/tx/<tx>`) a
`docs/evidencias/transaccion-onchain.md`. Tomar captura.

- [ ] **Step 5: Commit**

```bash
git add docs/evidencias/transaccion-onchain.md
git commit -m "docs(evidencias): transacción real registrada en Polygon Amoy"
```

---

## Task 17: Backend — esquemas y almacenamiento en memoria

**Files:**
- Create: `backend/schemas.py`, `backend/store.py`

- [ ] **Step 1: Crear `backend/schemas.py`**

```python
from pydantic import BaseModel
from typing import Any


class ReglaIn(BaseModel):
    texto: str
    schema_vars: dict[str, str]  # nombre -> tipo


class PostulantesIn(BaseModel):
    postulantes: list[dict[str, Any]]


class EvaluarOut(BaseModel):
    ranking: list[dict[str, Any]]
    no_elegibles: list[dict[str, Any]]
```

- [ ] **Step 2: Crear `backend/store.py`**

```python
"""Almacenamiento simple en memoria para el MVP (sin base de datos)."""

_estado = {"motor": None, "texto_regla": None, "postulantes": []}


def set_motor(motor, texto):
    _estado["motor"] = motor
    _estado["texto_regla"] = texto


def get_motor():
    return _estado["motor"], _estado["texto_regla"]


def set_postulantes(lista):
    _estado["postulantes"] = lista


def get_postulantes():
    return _estado["postulantes"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/schemas.py backend/store.py
git commit -m "feat(backend): esquemas pydantic y store en memoria"
```

---

## Task 18: Backend — endpoints y orquestación

**Files:**
- Create: `backend/main.py`
- Test: `backend/tests/test_api.py`

- [ ] **Step 1: Escribir el test que falla**

```python
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

SCHEMA = {"ingreso_familiar": "numero", "promedio": "numero",
          "integrantes_familia": "numero", "distancia_km": "numero"}


def test_flujo_completo():
    r = client.post("/reglas", json={
        "texto": "SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible",
        "schema_vars": SCHEMA,
    })
    assert r.status_code == 200

    r = client.post("/postulantes", json={"postulantes": [
        {"id": 1, "ingreso_familiar": 100000, "promedio": 9, "integrantes_familia": 5, "distancia_km": 80},
        {"id": 2, "ingreso_familiar": 500000, "promedio": 9, "integrantes_familia": 1, "distancia_km": 2},
        {"id": 3, "ingreso_familiar": 250000, "promedio": 8, "integrantes_familia": 2, "distancia_km": 10},
    ]})
    assert r.status_code == 200

    r = client.post("/evaluar", json={})
    assert r.status_code == 200
    data = r.json()
    ids_ranking = [p["id"] for p in data["ranking"]]
    assert ids_ranking == [1, 3]              # el 2 no es elegible (ingreso alto)
    assert data["ranking"][0]["score"] >= data["ranking"][1]["score"]
    assert "certificado" in data["ranking"][0]


def test_regla_invalida_da_400():
    r = client.post("/reglas", json={
        "texto": "SI inexistente < 5 ENTONCES elegible",
        "schema_vars": SCHEMA,
    })
    assert r.status_code == 400
```

- [ ] **Step 2: Correr y verificar que falla**

Run: `pytest backend/tests/test_api.py -v`
Expected: FAIL — `No module named 'backend.main'`.

- [ ] **Step 3: Implementar `backend/main.py`**

```python
from fastapi import FastAPI, HTTPException
from backend.schemas import ReglaIn, PostulantesIn
from backend import store
from dsl.engine import compilar_regla
from dsl.errors import ErrorDSL
from ia.modelo import priorizar
from contracts.web3_client import registrar_decision

app = FastAPI(title="VeriBeca API")


@app.post("/reglas")
def cargar_reglas(body: ReglaIn):
    try:
        motor = compilar_regla(body.texto, body.schema_vars)
    except ErrorDSL as e:
        raise HTTPException(status_code=400, detail=str(e))
    store.set_motor(motor, body.texto)
    return {"ok": True, "mensaje": "Regla válida y cargada"}


@app.post("/postulantes")
def cargar_postulantes(body: PostulantesIn):
    store.set_postulantes(body.postulantes)
    return {"ok": True, "cantidad": len(body.postulantes)}


@app.post("/evaluar")
def evaluar():
    motor, texto = store.get_motor()
    if motor is None:
        raise HTTPException(status_code=400, detail="No hay regla cargada")
    postulantes = store.get_postulantes()
    elegibles, no_elegibles = [], []
    for p in postulantes:
        if motor.evaluar(p):
            elegibles.append(p)
        else:
            no_elegibles.append(p)
    ranking = priorizar(elegibles)
    for p in ranking:
        cert = registrar_decision(p, texto, True)
        p["certificado"] = cert
    return {"ranking": ranking, "no_elegibles": no_elegibles}
```

- [ ] **Step 4: Crear `backend/tests/__init__.py` vacío y correr**

Run: `pytest backend/tests/test_api.py -v`
Expected: PASS (la blockchain cae en fallback porque no hay `CONTRACT_ADDRESS` en el entorno de test).

- [ ] **Step 5: Commit**

```bash
git add backend/main.py backend/tests/
git commit -m "feat(backend): endpoints /reglas /postulantes /evaluar con orquestación"
```

---

## Task 19: Levantar el backend y probar manualmente

- [ ] **Step 1: Iniciar el servidor**

Run: `uvicorn backend.main:app --reload`
Expected: servidor en http://127.0.0.1:8000 ; docs en /docs.

- [ ] **Step 2: Probar desde /docs**

Cargar una regla de `data/reglas_ejemplo.txt`, cargar 2-3 postulantes y llamar `/evaluar`.
Verificar que devuelve ranking con `score` y `certificado`.

- [ ] **Step 3: Capturar evidencia**

Guardar captura de `/docs` con la respuesta de `/evaluar` en `docs/evidencias/`.

---

## Task 20: Frontend Streamlit

**Files:**
- Create: `frontend/app.py`

- [ ] **Step 1: Implementar `frontend/app.py`**

```python
import requests
import pandas as pd
import streamlit as st

API = "http://127.0.0.1:8000"

SCHEMA = {
    "ingreso_familiar": "numero", "promedio": "numero",
    "integrantes_familia": "numero", "distancia_km": "numero",
    "trabaja": "booleano", "carrera": "texto",
}

st.set_page_config(page_title="VeriBeca", page_icon="🎓", layout="wide")
st.title("🎓 VeriBeca — Asignación transparente de becas")

st.header("1. Definí la regla de elegibilidad")
regla = st.text_area(
    "Regla (DSL)",
    "SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible",
)
if st.button("Validar y cargar regla"):
    r = requests.post(f"{API}/reglas", json={"texto": regla, "schema_vars": SCHEMA})
    if r.status_code == 200:
        st.success("✅ Regla válida y cargada")
    else:
        st.error(f"❌ {r.json()['detail']}")

st.header("2. Cargá los postulantes (CSV)")
archivo = st.file_uploader("CSV de postulantes", type="csv")
if archivo is not None:
    df = pd.read_csv(archivo)
    # normalizar booleanos y tipos
    if "trabaja" in df.columns:
        df["trabaja"] = df["trabaja"].astype(str).str.lower().map({"true": True, "false": False})
    st.dataframe(df.head())
    if st.button("Cargar postulantes"):
        r = requests.post(f"{API}/postulantes", json={"postulantes": df.to_dict("records")})
        st.success(f"✅ {r.json()['cantidad']} postulantes cargados")

st.header("3. Evaluar y priorizar")
if st.button("Evaluar"):
    r = requests.post(f"{API}/evaluar", json={})
    data = r.json()
    st.subheader("Ranking de elegibles (por vulnerabilidad)")
    for i, p in enumerate(data["ranking"], 1):
        cert = p["certificado"]
        modo = cert["modo"]
        with st.expander(f"#{i} — {p.get('nombre', p['id'])} · score {p['score']}"):
            st.write(p)
            if modo == "onchain":
                st.markdown(f"🔗 [Ver transacción](https://amoy.polygonscan.com/tx/{cert['tx']})")
            else:
                st.info(f"Certificado (fallback local): `{cert['hash']}`")
    st.subheader("No elegibles")
    st.write([p.get("nombre", p["id"]) for p in data["no_elegibles"]])
```

- [ ] **Step 2: Levantar y probar**

Run (con el backend ya corriendo en otra terminal): `streamlit run frontend/app.py`
Expected: abre la app; flujo completo regla → CSV (`data/postulantes.csv`) → evaluar funciona.

- [ ] **Step 3: Commit**

```bash
git add frontend/app.py
git commit -m "feat(frontend): UI Streamlit del flujo completo"
```

---

## Task 21: Capturas de evidencia del MVP

**Files:**
- Create: `docs/evidencias/` (capturas)

- [ ] **Step 1: Capturar el flujo en Streamlit**

Tomar capturas de: (a) validación de regla OK, (b) error de type-checker con una regla mala,
(c) ranking de elegibles con scores, (d) certificado on-chain / link al explorer.

- [ ] **Step 2: Capturar tests en verde**

Run: `pytest -v`
Tomar captura de toda la suite pasando.

- [ ] **Step 3: Commit**

```bash
git add docs/evidencias/
git commit -m "docs(evidencias): capturas del MVP y suite de tests"
```

---

## Task 22: README principal

**Files:**
- Create: `README.md`

- [ ] **Step 1: Escribir `README.md`** con: descripción, problema, solución, cómo cumple la
consigna (tabla de unidades), arquitectura (diagrama ASCII del spec), stack, instrucciones de
instalación y ejecución (`pip install -r requirements.txt`, `python ia/generar_dataset.py`,
`uvicorn backend.main:app`, `streamlit run frontend/app.py`), cómo correr tests (`pytest`),
estructura del repo, equipo y roles, y enlaces a los documentos de `docs/`.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: README principal"
```

---

## Task 23: Lean Canvas

**Files:**
- Create: `docs/lean-canvas.md`

- [ ] **Step 1: Escribir `docs/lean-canvas.md`** con los 9 bloques: Problema, Segmentos de
clientes, Propuesta de valor única, Solución, Canales, Fuentes de ingresos/sostenibilidad,
Estructura de costos, Métricas clave, Ventaja diferencial. Usar el contenido del spec y del
documento de la semana 1.

- [ ] **Step 2: Commit**

```bash
git add docs/lean-canvas.md
git commit -m "docs: Lean Canvas"
```

---

## Task 24: Memoria Técnica

**Files:**
- Create: `docs/memoria-tecnica.md`

- [ ] **Step 1: Escribir `docs/memoria-tecnica.md`** (4-6 páginas) siguiendo la estructura de la
guía UCH: 1) Problema y oportunidad, 2) Solución propuesta, 3) MVP desarrollado, 4) Componentes
tecnológicos (IA, Blockchain, integración con ≥3 líneas temáticas de la materia), 5) Innovación e
impacto, 6) Viabilidad y sustentabilidad, 7) Trabajo en equipo (roles de las 3 personas), 8)
Aprendizajes y propuestas descartadas, 9) Fuentes y referencias. Anticipar las preguntas del
jurado listadas en la guía.

- [ ] **Step 2: Commit**

```bash
git add docs/memoria-tecnica.md
git commit -m "docs: Memoria Técnica"
```

---

## Task 25: Pitch Deck

**Files:**
- Create: `docs/pitch-deck.md`

- [ ] **Step 1: Escribir `docs/pitch-deck.md`** (≤10 slides, una sección por slide):
1) Título/equipo, 2) Problema, 3) Magnitud/evidencia, 4) Solución, 5) Demo (cómo funciona),
6) Cómo cumple la consigna (DSL+tipos+compilador+blockchain+IA), 7) Innovación/diferencial,
8) Impacto y métricas, 9) Viabilidad/sostenibilidad, 10) Cierre + llamado a la acción.
Indicar para cada slide el texto clave y qué mostrar.

- [ ] **Step 2: Commit**

```bash
git add docs/pitch-deck.md
git commit -m "docs: Pitch Deck"
```

---

## Task 26: Guion del video demo

**Files:**
- Create: `docs/guion-video.md`

- [ ] **Step 1: Escribir `docs/guion-video.md`** (≤3 min): segundos por bloque (problema 30s,
solución 45s, demo en vivo 60s, cumplimiento de consigna 30s, cierre 15s), quién habla en cada
parte (las 2 personas que exponen), y qué se muestra en pantalla.

- [ ] **Step 2: Commit**

```bash
git add docs/guion-video.md
git commit -m "docs: guion del video demo"
```

---

## Task 27: Pulido final y verificación

- [ ] **Step 1: Correr toda la suite**

Run: `pytest -v`
Expected: TODOS los tests en verde.

- [ ] **Step 2: Verificar el flujo end-to-end** (backend + frontend) una vez más, idealmente con
la blockchain on-chain activa para tener la tx real en el video.

- [ ] **Step 3: Revisar el repo**: README claro, todos los docs presentes, `.env` NO commiteado,
estructura ordenada. Confirmar que el repo es público en GitHub.

- [ ] **Step 4: Grabar el video** siguiendo `docs/guion-video.md` y subir el link al README.

- [ ] **Step 5: Commit final**

```bash
git add -A
git commit -m "chore: pulido final, link de video y verificación"
```

---

## Self-Review (cobertura del spec)

- DSL (lexer/parser/types/interpreter/engine): Tareas 2-10 ✓
- Backend FastAPI (reglas/postulantes/evaluar/certificado): Tareas 17-19 ✓
- IA scikit-learn (scoring + priorización): Tareas 11-13 ✓
- Blockchain (contrato + web3 + fallback + tx real): Tareas 14-16 ✓
- Frontend Streamlit (3 pantallas): Tarea 20 ✓
- Dataset sintético + reglas ejemplo: Tareas 10-11 ✓
- Evidencias del MVP: Tareas 16, 19, 21 ✓
- Documentación (README, Lean Canvas, Memoria, Pitch, Guion video): Tareas 22-26 ✓
- Cobertura de las 4 unidades + IA + Blockchain: tabla en spec §7, implementada en DSL+contracts+ia ✓
- Criterios de éxito del spec §12: cubiertos por Tareas 10 (tests), 18 (ranking), 16 (tx real), 27 (demo) ✓
