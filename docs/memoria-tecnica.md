# Memoria Técnica — VeriBeca

**Materia:** Teoría de Computación 2 · Hackathon · Universidad Champagnat
**Equipo:** 3 integrantes
**Repositorio:** (link al repo público de GitHub)

---

## 1. Problema y oportunidad

**Problema identificado.** En universidades, municipios y ONGs, la asignación de becas,
subsidios y ayudas sociales se percibe como poco transparente: los criterios de elegibilidad
suelen ser ambiguos, la evaluación es manual y lenta, y existen sospechas —a veces
fundadas— de favoritismo o clientelismo. Cuando un postulante queda afuera, no tiene forma
simple de auditar *por qué*, ni garantía de que la regla aplicada haya sido la misma para todos.

**Usuarios afectados.** Por un lado, las **instituciones** que asignan ayudas (áreas de
bienestar estudiantil, municipios, ONGs), que deben decidir de forma justa, rápida y
defendible ante auditorías o reclamos. Por otro, los **postulantes**, que reciben una decisión
que hoy es difícil de verificar.

**Magnitud y relevancia.** Las becas y ayudas sociales mueven presupuestos significativos y
afectan directamente la continuidad educativa y el bienestar de poblaciones vulnerables. Un
proceso opaco erosiona la confianza institucional y puede dejar a personas que califican fuera
del beneficio por errores o inconsistencias.

**Evidencia que justifica la necesidad.** La discrecionalidad y la falta de trazabilidad en la
asignación de fondos públicos y sociales es un problema recurrente y documentado en gestión
pública. La demanda de transparencia y rendición de cuentas (open government) es creciente.

**Preguntas del jurado anticipadas:**
- *¿Cómo validaron que el problema existe?* A partir de la experiencia conocida en procesos de
  becas (criterios poco claros, decisiones no auditables) y de la demanda general de
  transparencia en la asignación de fondos. Un MVP como este es validable con una entrevista a
  un área de bienestar estudiantil.
- *¿Por qué vale la pena resolverlo?* Porque afecta decisiones sensibles sobre poblaciones
  vulnerables y porque la falta de auditoría genera conflictos y desconfianza.
- *¿Quién sufre el problema?* Tanto las instituciones (exposición ante reclamos) como los
  postulantes (decisiones no verificables).

## 2. Solución propuesta

**Producto.** VeriBeca es una plataforma donde la institución define sus criterios de
elegibilidad en un **DSL (lenguaje de dominio específico) tipado**, el sistema los valida y
aplica automáticamente sobre todos los postulantes, una **IA** prioriza a los elegibles por
vulnerabilidad, y **cada decisión se sella con un hash registrado en blockchain** como
certificado de auditoría.

**Funcionamiento general.**
1. La institución escribe una regla, p. ej. `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`.
2. El **type-checker** valida la regla antes de aplicarla (detecta variables inexistentes,
   comparaciones de tipos incompatibles, etc.).
3. El **intérprete** evalúa la regla contra los datos de cada postulante (elegible / no elegible).
4. La **IA** ordena a los elegibles por un score de vulnerabilidad socioeconómica.
5. Por cada decisión se calcula `hash(datos + regla + resultado)` y se registra en un smart
   contract en testnet; queda un certificado verificable por cualquiera.

**Principales características.** Reglas declarativas y legibles; validación de tipos previa;
aplicación automática y consistente; priorización transparente; trazabilidad inmutable.

**Diferencias respecto a alternativas.** Las planillas y sistemas internos actuales no validan
las reglas formalmente ni dejan evidencia inalterable. VeriBeca combina un lenguaje verificable
con un registro inmutable, algo que una hoja de cálculo o un sistema cerrado no ofrecen.

**Preguntas del jurado anticipadas:**
- *¿Qué los diferencia?* La auditoría inmutable de cada decisión + reglas tipadas que evitan
  errores antes de aplicarlas.
- *¿Por qué elegirían esta propuesta?* Porque reduce el tiempo de evaluación y, sobre todo,
  porque permite defender públicamente cada decisión con evidencia verificable.

## 3. MVP desarrollado

**Alcance real del MVP.** Se implementó el flujo completo de punta a punta:

- **Motor DSL 100% funcional y testeado**: lexer, parser (AST), type-checker e intérprete.
- **Backend FastAPI** con endpoints `/reglas`, `/postulantes`, `/evaluar`.
- **Modelo de IA** de scoring/priorización (scikit-learn) sobre dataset sintético.
- **Smart contract** en Solidity + cliente web3 con **fallback local** para que la demo nunca
  se caiga.
- **Frontend Streamlit** que une todo el flujo.

**Evidencia de funcionamiento.** Prueba end-to-end sobre 100 postulantes sintéticos: la regla
se valida, 24 resultan elegibles, se priorizan por score y cada uno recibe un certificado.
Ver [evidencias/smoke-test-e2e.md](evidencias/smoke-test-e2e.md). Suite de **27 tests** en verde.

**Funcionalidades planificadas (futuras versiones).** Autenticación y multi-institución,
persistencia en base de datos, despliegue en mainnet/L2 de producción, panel de reportería,
importadores desde sistemas existentes, y soporte de reglas con más operadores y funciones.

**Preguntas del jurado anticipadas:**
- *¿Qué funciona actualmente?* Todo el pipeline: escribir y validar una regla, evaluar
  postulantes, priorizarlos con IA y generar el certificado (on-chain o fallback).
- *¿Qué quedó pendiente?* Autenticación, persistencia real, despliegue productivo y reportería.

## 4. Componentes tecnológicos

**Tecnologías y arquitectura.**

```
[Streamlit UI]  ──>  [FastAPI backend]
                          ├─ Motor DSL:  lexer → parser → AST → type-checker → intérprete
                          ├─ IA (scikit-learn): scoring de prioridad sobre elegibles
                          └─ Web3: hash(decisión) → Smart Contract (Ethereum Sepolia) [+ fallback local]
```

- **Lenguaje/Framework:** Python + FastAPI (backend), Streamlit (frontend).
- **Tests:** pytest.

**Inteligencia Artificial.**
- *Qué usamos:* `scikit-learn` (regresión lineal como demostración de aprendizaje + un score
  interpretable basado en indicadores normalizados de vulnerabilidad).
- *Por qué la elegimos:* simplicidad e **interpretabilidad** — en decisiones sensibles, poder
  explicar por qué un postulante tiene mayor prioridad es más importante que un modelo opaco.
  Con pocos datos, un score transparente es defendible ante el jurado y ante un reclamo.
- *Qué valor aporta:* ordena a los elegibles por necesidad, de forma consistente y explicable.

**Blockchain.**
- *Cómo se usó:* un smart contract `AuditoriaBecas` (Solidity) en la **testnet Ethereum Sepolia**.
  Por cada decisión se calcula `sha256(datos + regla + resultado)` y se registra con
  `registrar(bytes32 hash)`, emitiendo un evento con timestamp. La interacción es vía `web3.py`.
- *Qué problema resuelve:* garantiza que la decisión **no fue alterada** después; cualquiera
  puede verificar el hash en el explorer.
- *Evidencia de funcionamiento:* transacción verificable en el explorer de Sepolia (ver
  `docs/evidencias/`). Si el RPC/faucet falla, un **fallback local** registra el mismo hash en
  un archivo, de modo que el flujo nunca se interrumpe.

**Integración con contenidos de la materia (≥3 líneas temáticas).**
1. **Lenguajes de programación (Unidad I):** diseño de un DSL propio con su gramática.
2. **Sistemas de tipos (Unidad II):** type-checker que valida las reglas antes de aplicarlas.
3. **Diseño de compiladores (Unidad III):** pipeline `lexer → parser → AST → intérprete`.
4. **Seguridad / Blockchain (Unidad IV):** hashing y registro inmutable en un smart contract.

**Preguntas del jurado anticipadas:**
- *¿Dónde se aplican los conceptos teóricos?* En el motor DSL (lexer/parser/tipos/intérprete) y
  en el smart contract; son conceptos directos de las unidades de la materia.
- *¿Por qué esa arquitectura?* Módulos desacoplados (el DSL es un paquete puro, testeable solo;
  el backend solo orquesta), lo que facilita probar cada parte y reemplazar piezas (p. ej. la
  blockchain) sin tocar el resto.

## 5. Innovación e impacto

**Aspectos innovadores / originales.** Combinar un **lenguaje verificable de reglas** con
**registro inmutable** y **priorización por IA** en un único flujo aplicado a un problema social
concreto. No es "blockchain por moda": el hash on-chain resuelve específicamente la
auditabilidad.

**Ventajas competitivas.** Trazabilidad verificable por terceros; reglas que no se pueden
aplicar mal por errores de tipos; consistencia total entre evaluadores.

**Impacto esperado.**
- *Beneficiarios:* postulantes (decisiones justas y verificables) e instituciones (procesos
  defendibles).
- *Impacto social:* más confianza en las instituciones, menos discrecionalidad.
- *Impacto económico:* reducción drástica del tiempo de evaluación frente al proceso manual.
- *Impacto ambiental:* uso de una testnet PoS (Ethereum Sepolia) de bajo consumo energético frente a cadenas PoW. En producción puede usarse una L2 (ej. Polygon) para minimizar costos y energía.

**Preguntas del jurado anticipadas:**
- *¿Cómo medirían el éxito?* Tiempo de evaluación reducido, 100% de decisiones con certificado
  verificable, y reducción de reclamos resueltos sin evidencia.
- *¿Qué cambio concreto esperan?* Pasar de "confíen en nosotros" a "verifíquenlo ustedes mismos".

## 6. Viabilidad y sustentabilidad

- **Factibilidad técnica:** demostrada — el MVP funciona end-to-end con tecnologías maduras y
  gratuitas.
- **Factibilidad económica:** costos bajos (la testnet es gratuita; en producción, una L2 tiene
  gas mínimo); modelo SaaS por institución.
- **Factibilidad operativa:** la institución solo necesita escribir reglas y cargar postulantes.

**Recursos necesarios:** equipo de desarrollo, hosting del backend, y una wallet para firmar
transacciones. **Posibles aliados:** áreas de bienestar universitario, municipios, fundaciones
de transparencia. **Estrategia de crecimiento:** empezar open-source con una universidad piloto
y expandir a municipios/ONGs.

**Preguntas del jurado anticipadas:**
- *¿Cómo se sostiene en el tiempo?* Suscripción SaaS + servicios de implementación.
- *¿Quién pagaría?* Las instituciones que asignan las ayudas, que ganan eficiencia y reputación.

## 7. Trabajo en equipo

Equipo de **3 integrantes**; las 3 desarrollan y 2 exponen el pitch.

| Rol | Responsabilidades |
| :--- | :--- |
| **Integrante 1 — Lenguajes, Compiladores y Tipos** | Diseño e implementación del DSL: lexer, parser, AST, type-checker, intérprete (Unidades I, II, III). |
| **Integrante 2 — IA y Backend** | Dataset sintético, modelo de scoring, API FastAPI que orquesta el flujo. |
| **Integrante 3 — Blockchain, Frontend y Documentación** | Smart contract, cliente web3 con fallback, UI Streamlit, documentación. |

**Organización y metodología.** Trabajo ágil con backlog por épicas (Definición → MVP →
Demoday), módulos desacoplados que permitieron desarrollar en **paralelo**, y commits
frecuentes. Las decisiones se tomaron por consenso priorizando un MVP demostrable sobre el
alcance amplio.

**Preguntas del jurado anticipadas:**
- *¿Cómo distribuyeron las tareas?* Por módulos independientes (DSL / IA+backend /
  blockchain+frontend), lo que permitió avanzar en paralelo.
- *¿Cómo tomaron decisiones?* Priorizando YAGNI: primero el núcleo (DSL) y un flujo end-to-end
  demostrable, dejando lo accesorio para futuras versiones.

## 8. Aprendizajes y propuestas descartadas

- **Idea descartada — entrenar un modelo de IA complejo:** se descartó por falta de datos
  reales y porque la interpretabilidad es prioritaria en decisiones sensibles. Se optó por un
  score transparente + demostración con scikit-learn.
- **Idea descartada — desplegar en mainnet:** innecesario y costoso para un MVP; una testnet
  (Ethereum Sepolia) demuestra el concepto sin riesgo ni gasto.
- **Idea descartada — frontend en React:** mayor tiempo de desarrollo; Streamlit da una UI
  presentable en una fracción del esfuerzo, adecuada para el plazo.
- **Aprendizajes:** el valor de desacoplar módulos (testear el DSL aislado aceleró todo), la
  importancia de un fallback para que una demo en vivo no dependa de la red, y el diseño de un
  type-checker simple pero efectivo.

## 9. Fuentes y referencias

- Documentación de Python, FastAPI, scikit-learn, Streamlit y web3.py.
- Documentación de Ethereum (testnet Sepolia) y Solidity.
- Conceptos de las unidades de Teoría de Computación 2 (lenguajes, tipos, compiladores,
  seguridad/blockchain).
- Bibliografía clásica de compiladores (lexer/parser/AST/intérprete).
