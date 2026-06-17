# 🎓 VeriBeca

### Asignación transparente de becas y ayudas sociales con DSL tipado, IA y Blockchain

Proyecto de **Teoría de Computación 2** — Hackathon, Universidad Champagnat.

VeriBeca permite que una institución defina sus **criterios de elegibilidad** en un lenguaje
propio simple (un DSL tipado), el sistema los **valida y aplica automáticamente**, una **IA**
prioriza a quienes califican según vulnerabilidad, y **cada decisión queda registrada de forma
inmutable en blockchain** como certificado de auditoría verificable por cualquiera.

---

## El problema

La asignación de becas, subsidios y ayudas sociales se percibe como poco transparente:
criterios ambiguos, evaluación manual lenta y sospechas de favoritismo. Cuando alguien queda
afuera, no hay forma simple de auditar *por qué*, ni garantía de que la regla aplicada fue la
misma para todos.

## La solución

1. La institución escribe sus reglas en el **DSL** (ej: `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`).
2. Un **type-checker** valida que las reglas estén bien formadas *antes* de aplicarlas.
3. El **intérprete** evalúa cada postulante y marca a los elegibles.
4. La **IA** ordena a los elegibles por un score de vulnerabilidad.
5. Por cada decisión se calcula un **hash** y se registra en un **smart contract** (testnet
   Polygon Amoy), generando un certificado de auditoría verificable.

## Cómo cumple la consigna de la materia

| Unidad / Eje | Dónde se aplica en VeriBeca |
| :--- | :--- |
| **I. Lenguajes de programación** | DSL propio de reglas de elegibilidad |
| **II. Sistemas de tipos** | type-checker del DSL (tipos `numero`, `booleano`, `texto`) |
| **III. Diseño de compiladores** | pipeline `lexer → parser → AST → type-checker → intérprete` |
| **IV. Seguridad / Blockchain** | hash de cada decisión + smart contract en testnet |
| **Inteligencia Artificial** | scoring/priorización por vulnerabilidad (scikit-learn) |

## Arquitectura

```
[Streamlit UI]  ──>  [FastAPI backend]
                          ├─ Motor DSL:  lexer → parser → AST → type-checker → intérprete
                          ├─ IA (scikit-learn): scoring de prioridad sobre elegibles
                          └─ Web3: hash(decisión) → Smart Contract (Polygon Amoy) [+ fallback local]
```

## Stack tecnológico

Python · FastAPI · scikit-learn · pandas · Solidity · Polygon Amoy (testnet) · web3.py · Streamlit · pytest.

## Estructura del repositorio

```
veribeca/
├─ dsl/           # motor del lenguaje: lexer, parser, type-checker, intérprete
├─ ia/            # dataset sintético + modelo de scoring de vulnerabilidad
├─ contracts/     # smart contract Solidity + cliente web3 con fallback local
├─ backend/       # API FastAPI que orquesta DSL + IA + blockchain
├─ frontend/      # interfaz Streamlit
├─ tests/         # tests del DSL
├─ data/          # dataset sintético y reglas de ejemplo
└─ docs/          # Lean Canvas, Memoria Técnica, Pitch Deck, guion de video, evidencias
```

## Cómo ejecutarlo

> Requiere Python 3.10+.

```bash
# 1. Crear entorno e instalar dependencias
python -m venv .venv
# Windows:  .venv\Scripts\activate     Linux/Mac:  source .venv/bin/activate
pip install -r requirements.txt

# 2. Generar el dataset sintético de postulantes
python ia/generar_dataset.py

# 3. Levantar el backend (en una terminal)
uvicorn backend.main:app --reload

# 4. Levantar el frontend (en otra terminal)
streamlit run frontend/app.py
```

En la UI: cargá una regla (hay ejemplos en `data/reglas_ejemplo.txt`), subí el CSV
`data/postulantes.csv`, y presioná **Evaluar**.

### Blockchain (opcional para la demo)

Sin configurar nada, los certificados se generan en modo **fallback local** (la demo funciona
igual). Para registrar en la testnet real, copiá `.env.example` a `.env` y completá
`AMOY_RPC_URL`, `PRIVATE_KEY` y `CONTRACT_ADDRESS`. Ver instrucciones detalladas en
[docs/memoria-tecnica.md](docs/memoria-tecnica.md).

## Cómo correr los tests

```bash
pytest -q
```

Suite actual: **27 tests** (DSL 20 · IA 3 · backend 2 · contracts 2).

## Documentación

- [Lean Canvas](docs/lean-canvas.md)
- [Memoria Técnica](docs/memoria-tecnica.md)
- [Pitch Deck](docs/pitch-deck.md)
- [Guion del video demo](docs/guion-video.md)
- [Evidencias del MVP](docs/evidencias/)

## Equipo

Equipo de 3 integrantes. Roles y organización del trabajo en la
[Memoria Técnica, sección 7](docs/memoria-tecnica.md).

## Video demo

> _(Agregar enlace al video cuando esté grabado.)_
