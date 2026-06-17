# Pitch Deck — VeriBeca (≤10 slides)

> Guía de contenido por slide. Pasar a Canva/Google Slides/PowerPoint. Una idea por slide,
> poco texto, apoyarse en el diagrama y la demo.

---

### Slide 1 — Título
- **VeriBeca** — Asignación transparente de becas y ayudas sociales.
- Subtítulo: *DSL tipado + IA + Blockchain.*
- Equipo (3 integrantes) · Teoría de Computación 2 · Universidad Champagnat.
- *Visual:* logo / ícono 🎓.

### Slide 2 — El problema
- La asignación de becas y ayudas se percibe como **opaca**: criterios ambiguos, evaluación
  manual, sospechas de favoritismo.
- "Cuando alguien queda afuera, no puede auditar **por qué**."
- *Visual:* ilustración de una decisión "caja negra".

### Slide 3 — Magnitud / por qué importa
- Afecta presupuestos significativos y a poblaciones vulnerables.
- La falta de trazabilidad genera **desconfianza** y conflictos.
- Demanda creciente de transparencia (open government).
- *Visual:* 2-3 datos/íconos de impacto.

### Slide 4 — La solución
- La institución escribe reglas en un **lenguaje simple y verificable**.
- El sistema las **valida, aplica y prioriza** automáticamente.
- Cada decisión queda **sellada en blockchain** → verificable por cualquiera.
- *Visual:* los 5 pasos del flujo en una fila.

### Slide 5 — Cómo funciona (demo)
- Mostrar: escribir una regla → validación → ranking de elegibles → certificado on-chain.
- Ejemplo: `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`.
- *Visual:* captura de la UI Streamlit / demo en vivo.

### Slide 6 — Cómo cumple la consigna
- Tabla: **Lenguajes** (DSL) · **Tipos** (type-checker) · **Compiladores** (lexer→parser→AST→intérprete) · **Blockchain** (hash + smart contract) · **IA** (scoring).
- "4 unidades + IA + Blockchain integradas en un solo flujo."
- *Visual:* el diagrama de arquitectura.

### Slide 7 — Innovación y diferencial
- No es "blockchain de moda": el hash on-chain resuelve **auditabilidad** concreta.
- Reglas **tipadas** que evitan errores antes de afectar a personas reales.
- Difícil de copiar: combina compiladores + blockchain + IA.

### Slide 8 — Impacto y métricas
- −80% tiempo de evaluación vs manual · 100% de decisiones verificables.
- Beneficiarios: postulantes (justicia) e instituciones (procesos defendibles).
- Impacto ambiental: L2 de bajo consumo (Polygon).

### Slide 9 — Viabilidad y sostenibilidad
- Técnica: MVP funcionando end-to-end (27 tests, transacción real en testnet).
- Económica: SaaS por institución + servicios; costos bajos.
- Aliados: bienestar universitario, municipios, fundaciones de transparencia.

### Slide 10 — Cierre
- "De *'confíen en nosotros'* a *'verifíquenlo ustedes mismos'*."
- Llamado a la acción: piloto con una universidad.
- Link al repo + gracias + preguntas.
