# VeriBeca — Documento de Diseño (Spec)

**Fecha:** 2026-06-17
**Materia:** Teoría de Computación 2 — Hackathon (Universidad Champagnat)
**Equipo:** 3 personas (las 3 desarrollan; 2 exponen el pitch)
**Plazo objetivo:** lo antes posible (tope blando: 8 días; meta: ~5 días con trabajo en paralelo)

---

## 1. Resumen

**VeriBeca** es una plataforma para asignar becas y ayudas sociales de forma transparente y
auditable. La institución define sus criterios de elegibilidad en un **DSL tipado** propio; el
sistema los valida (type-checker) y los aplica automáticamente (intérprete) sobre los
postulantes; una **IA** prioriza a los elegibles según vulnerabilidad; y cada decisión se sella
con un **hash registrado en blockchain** (testnet) como certificado de auditoría verificable.

El proyecto integra de forma real las 4 unidades de la materia + IA + Blockchain en un único
flujo, lo que es el criterio central de evaluación.

## 2. Problema

La asignación de becas/subsidios/ayudas en universidades, municipios y ONGs se percibe como
poco transparente: criterios ambiguos, evaluación manual lenta y sospechas de favoritismo.
Cuando alguien queda afuera no hay forma simple de auditar *por qué*, ni garantía de que la
regla aplicada fue la misma para todos.

- **Usuarios:** áreas de bienestar estudiantil, municipios, ONGs que distribuyen ayudas.
- **Impacto:** más confianza institucional, menos discrecionalidad, procesos auditables y
  decisiones más rápidas y justas.

## 3. Alcance del MVP

MVP **mínimo pero demostrable**: el núcleo (DSL) es 100% real y testeado; los componentes
accesorios son sólidos pero con mecanismos para que la demo nunca se rompa.

**Incluye:**
- DSL completo: lexer → parser → AST → type-checker → intérprete, con suite de tests.
- Backend FastAPI con endpoints para reglas, postulantes y evaluación.
- Modelo de IA (scikit-learn) de scoring/priorización sobre dataset sintético.
- Smart contract simple en Solidity desplegado en testnet Polygon Amoy + cliente web3 con
  **fallback local** (archivo JSON) para evitar fallos en vivo.
- Frontend en Streamlit con 3 pantallas.
- Documentación completa: README, Lean Canvas, Memoria Técnica, Pitch Deck, evidencias, video.

**Fuera de alcance (futuras versiones):** autenticación de usuarios, multi-institución,
persistencia en base de datos real, mainnet, despliegue productivo, panel de administración
avanzado.

## 4. Arquitectura

```
[Streamlit UI]  ──>  [FastAPI backend]
                          ├─ Motor DSL:  lexer → parser → AST → type-checker → intérprete
                          ├─ IA (scikit-learn): scoring de prioridad sobre elegibles
                          └─ Web3: hash(decisión) → Smart Contract (Polygon Amoy) [+ fallback local]
```

## 5. Componentes

Cada componente es una unidad aislada, con interfaz clara y testeable de forma independiente.

### 5.1 `dsl/` — Motor del lenguaje (núcleo, 100% real)
Paquete Python puro, sin dependencias del backend.
- `lexer.py`: texto → lista de tokens.
- `parser.py`: tokens → AST.
- `types.py`: type-checker que valida el AST (tipos: `numero`, `booleano`, `texto`, `enum`).
- `interpreter.py`: evalúa el AST contra los datos de un postulante → `elegible: bool`.
- **Sintaxis ejemplo:** `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`
- **Garantías del type-checker:** rechaza comparar texto con número, variables inexistentes,
  reglas mal formadas, antes de aplicarlas.
- **Tests:** casos válidos, errores de tipos, errores de sintaxis, evaluación correcta.

### 5.2 `backend/` — API (FastAPI)
Orquesta; no contiene lógica de negocio propia.
- `POST /reglas`: recibe texto DSL, lo valida con el type-checker, lo guarda en memoria/sesión.
- `POST /postulantes`: carga el dataset de postulantes (CSV/JSON).
- `POST /evaluar`: corre intérprete (elegibilidad) → IA (prioridad) → registra hash on-chain;
  devuelve ranking + referencia del certificado.
- `GET /certificado/{id}`: devuelve hash, tx/explorer link (o referencia de fallback).

### 5.3 `ia/` — Priorización (scikit-learn)
- Dataset sintético de postulantes: `ingreso_familiar`, `promedio`, `distancia_km`,
  `integrantes_familia`, etc.
- Modelo interpretable (p. ej. regresión logística o árbol) que produce un **score de
  vulnerabilidad** para ordenar a los **ya elegibles**.
- Se reporta importancia de variables para defender la decisión ante el jurado.

### 5.4 `contracts/` — Blockchain (Solidity + web3.py)
- Contrato `AuditoriaBecas`: función `registrar(bytes32 hash)` + evento con `timestamp`.
- Desplegado en **Polygon Amoy** (testnet).
- `web3_client.py`: calcula `hash(datos + regla + resultado)` y lo registra; si el RPC/faucet
  falla, escribe en `fallback_ledger.json` con la misma estructura → la demo nunca se cae.

### 5.5 `frontend/` — UI (Streamlit)
Tres pantallas:
1. Cargar y validar reglas (muestra errores del type-checker en vivo).
2. Ver resultados: tabla de postulantes con elegibilidad + ranking por prioridad.
3. Certificado on-chain: hash + link al explorer (o referencia de fallback).

## 6. Flujo de datos

1. Institución escribe reglas en el DSL.
2. El type-checker valida; si hay error, se muestra y se frena.
3. Se cargan postulantes (CSV).
4. `/evaluar`: el intérprete marca elegibles → la IA los prioriza por vulnerabilidad.
5. Por cada decisión se calcula un hash y se registra on-chain (o en fallback).
6. La UI muestra el ranking y el certificado verificable.

## 7. Cobertura de la consigna

| Requisito de la materia | Dónde se cumple |
|---|---|
| I. Lenguajes de programación | DSL de reglas de elegibilidad |
| II. Sistemas de tipos | type-checker del DSL |
| III. Diseño de compiladores | pipeline lexer → parser → AST → intérprete |
| IV. Seguridad / Blockchain | hash + smart contract en testnet |
| Inteligencia Artificial | scoring/priorización con scikit-learn |

## 8. Estructura del repositorio

```
veribeca/
├─ README.md
├─ dsl/            (paquete + tests)
├─ backend/
├─ ia/
├─ contracts/
├─ frontend/
├─ data/           (dataset sintético + reglas de ejemplo)
└─ docs/           (Lean Canvas, Memoria Técnica, Pitch Deck, evidencias, link video)
```

## 9. Stack tecnológico

- **Lenguaje principal:** Python 3.x
- **Backend:** FastAPI + Uvicorn
- **IA:** scikit-learn, pandas
- **Blockchain:** Solidity, Polygon Amoy testnet, web3.py
- **Frontend:** Streamlit
- **Tests:** pytest

## 10. Entregables de documentación (guía UCH)

- README principal del repo.
- Lean Canvas (Problema, Segmentos, Propuesta de valor única, Solución, Canales,
  Ingresos/sostenibilidad, Costos, Métricas clave, Ventaja diferencial).
- Memoria Técnica (4-6 páginas) según estructura recomendada por la guía.
- Pitch Deck (≤10 slides).
- Evidencias del MVP (capturas + tx on-chain).
- Guion + link del video demo (≤3 min).

## 11. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Falla de RPC/faucet en la demo | Fallback local de hashes (mismo formato). |
| Plazo corto (3 personas) | Paralelizar: DSL / IA+datos / blockchain+frontend. |
| DSL demasiado ambicioso | Gramática mínima viable (SI/Y/O/comparadores/ENTONCES elegible). |
| Video/documentación a último momento | Capturas de evidencia se generan al cerrar cada módulo. |

## 12. Criterios de éxito

- El DSL valida y evalúa reglas correctamente (tests en verde).
- `/evaluar` produce un ranking de postulantes elegibles priorizados.
- Al menos una transacción real verificable en el explorer de Polygon Amoy.
- Demo end-to-end funcionando en el video.
- Repositorio público y ordenado con toda la documentación obligatoria.
