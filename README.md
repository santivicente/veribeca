<div align="center">

# 🎓 VeriBeca

### Asignación transparente de becas y ayudas sociales con DSL tipado, IA y Blockchain

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-27%20passing-brightgreen)
![IA](https://img.shields.io/badge/IA-scikit--learn-F7931E)
![Blockchain](https://img.shields.io/badge/blockchain-Ethereum%20Sepolia-627EEA)
![MVP](https://img.shields.io/badge/MVP-funcional-success)

*Proyecto Final · Teoría de Computación 2 · Universidad Champagnat*

🎥 **[Ver video demo](https://drive.google.com/file/d/1Geh7Fkq4N-V72Xdu0PnhmSKgdIS6_0hP/view?usp=sharing)** &nbsp;·&nbsp; 🔗 **[Contrato en Etherscan](https://sepolia.etherscan.io/address/0xa37E9b370840F14f5E5C69Ff7B7119eCE3034176)** &nbsp;·&nbsp; 📄 **[Memoria Técnica](docs/memoria-tecnica.md)**

</div>

---

## 📑 Contenido

- [El problema](#-el-problema)
- [La solución](#-la-solución)
- [Cómo cumple la consigna](#-cómo-cumple-la-consigna-de-la-materia)
- [Arquitectura](#-arquitectura)
- [Evidencia de funcionamiento](#-evidencia-de-funcionamiento)
- [Cómo ejecutarlo](#-cómo-ejecutarlo)
- [Documentación](#-documentación)
- [Equipo](#-equipo)

---

## 🎯 El problema

La asignación de becas, subsidios y ayudas sociales se percibe como **poco transparente**:
criterios ambiguos, evaluación manual lenta y sospechas de favoritismo. Cuando alguien queda
afuera, **no hay forma simple de auditar *por qué***, ni garantía de que la regla aplicada haya
sido la misma para todos.

## 💡 La solución

VeriBeca permite que la institución defina sus criterios en un **lenguaje propio y tipado**, el
sistema los **valida y aplica automáticamente**, una **IA** prioriza por vulnerabilidad, y **cada
decisión queda sellada en blockchain** como certificado de auditoría verificable por cualquiera.

| Paso | Qué hace |
| :---: | :--- |
| **1** | La institución escribe la regla en el DSL: `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible` |
| **2** | Un **type-checker** valida que la regla esté bien formada *antes* de aplicarla |
| **3** | El **intérprete** evalúa a cada postulante y marca a los elegibles |
| **4** | La **IA** ordena a los elegibles por un score de vulnerabilidad |
| **5** | Se calcula un **hash** de la decisión y se registra en un **smart contract** (Ethereum Sepolia) |

## 🧩 Cómo cumple la consigna de la materia

Integra las **4 unidades del programa + IA + Blockchain** en un único flujo real:

| Unidad / Eje | Dónde se aplica en VeriBeca |
| :--- | :--- |
| **I. Lenguajes de programación** | DSL propio de reglas de elegibilidad |
| **II. Sistemas de tipos** | type-checker del DSL (tipos `numero`, `booleano`, `texto`) |
| **III. Diseño de compiladores** | pipeline `lexer → parser → AST → type-checker → intérprete` |
| **IV. Seguridad / Blockchain** | hash de cada decisión + smart contract en testnet |
| **Inteligencia Artificial** | scoring de vulnerabilidad con scikit-learn |

## 🏗️ Arquitectura

Módulos desacoplados, cada uno con una responsabilidad clara y testeable por separado:

```
[Streamlit UI]  ──>  [FastAPI backend]
                          ├─ Motor DSL:  lexer → parser → AST → type-checker → intérprete
                          ├─ IA (scikit-learn): scoring de prioridad sobre elegibles
                          └─ Web3: hash(decisión) → Smart Contract (Ethereum Sepolia) [+ fallback local]
```

**Stack:** Python · FastAPI · scikit-learn · pandas · Solidity · Ethereum Sepolia · web3.py · Streamlit · pytest

```
veribeca/
├─ dsl/         # motor del lenguaje: lexer, parser, type-checker, intérprete
├─ ia/          # dataset sintético + modelo de scoring de vulnerabilidad
├─ contracts/   # smart contract Solidity + cliente web3 con fallback local
├─ backend/     # API FastAPI que orquesta DSL + IA + blockchain
├─ frontend/    # interfaz Streamlit
├─ tests/       # suite de tests del DSL
├─ data/        # dataset sintético y reglas de ejemplo
└─ docs/        # Lean Canvas, Memoria Técnica, Pitch Deck, Informe, evidencias
```

## ✅ Evidencia de funcionamiento

- 🧪 **27 tests automáticos** en verde (DSL 20 · IA 3 · backend 2 · contracts 2).
- 📊 Sobre **100 postulantes** de prueba: evaluados y priorizados **24 elegibles** en segundos.
- ⛓️ **Smart contract real desplegado** en Ethereum Sepolia y **transacción verificable**:
  - Contrato: [`0xa37E9b37...CE3034176`](https://sepolia.etherscan.io/address/0xa37E9b370840F14f5E5C69Ff7B7119eCE3034176)
- 🛟 Si falla la red, el sistema sigue funcionando en **modo de respaldo** (la demo nunca se cae).

Más detalle en [docs/evidencias/](docs/evidencias/).

## 🚀 Cómo ejecutarlo

> Requiere **Python 3.10+**.

```bash
# 1. Clonar e instalar dependencias
git clone https://github.com/santivicente/veribeca.git
cd veribeca
python -m venv .venv
# Windows:  .venv\Scripts\activate     Linux/Mac:  source .venv/bin/activate
pip install -r requirements.txt

# 2. Levantar el backend (terminal 1)
uvicorn backend.main:app

# 3. Levantar el frontend (terminal 2)
streamlit run frontend/app.py
```

Se abre en **http://localhost:8501**. En la app: cargá una regla (ejemplos en
`data/reglas_ejemplo.txt`), subí el CSV `data/postulantes.csv` y presioná **Evaluar**.

**Tests:** `pytest -q`

> **Blockchain (opcional):** sin configurar nada, los certificados se generan en modo *fallback
> local*. Para registrar en la testnet real, copiá `.env.example` a `.env` y completá `RPC_URL`,
> `PRIVATE_KEY` y `CONTRACT_ADDRESS`.

## 📚 Documentación

| Documento | Descripción |
| :--- | :--- |
| [📊 Lean Canvas](docs/lean-canvas.md) | Modelo de negocio en una vista |
| [📄 Memoria Técnica](docs/memoria-tecnica.md) | Informe técnico completo (problema, solución, MVP, tecnología) |
| [📑 Informe del proyecto](docs/Informe-VeriBeca.pdf) | Informe ejecutivo en PDF |
| [🎤 Pitch Deck](docs/VeriBeca-Pitch.pptx) | Presentación (10 slides) |
| [📘 Guía de estudio](docs/Guia-VeriBeca.pdf) | Explicación detallada del DSL, IA y Blockchain |
| [🖼️ Evidencias del MVP](docs/evidencias/) | Pruebas end-to-end y registro on-chain |
| [🎥 Video demo](https://drive.google.com/file/d/1Geh7Fkq4N-V72Xdu0PnhmSKgdIS6_0hP/view?usp=sharing) | Demostración (≤3 min) |

## 👥 Equipo

Equipo de **3 integrantes** con metodología ágil (backlog por épicas, módulos desarrollados en
paralelo, commits frecuentes). Roles y organización en la
[Memoria Técnica, sección 7](docs/memoria-tecnica.md).

---

<div align="center">
<i>"De 'confíen en nosotros' a 'verifíquenlo ustedes mismos'."</i>
</div>
