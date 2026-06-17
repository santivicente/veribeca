# Guion del video demo — VeriBeca (≤3 min)

**Formato sugerido:** pantalla compartida (UI + explorer de Sepolia) con voz en off de las 2
personas que exponen. Total ≈ 2:40.

| Tiempo | Quién | Qué se dice | Qué se muestra en pantalla |
| :--- | :--- | :--- | :--- |
| **0:00–0:30** (Problema) | Expositor/a 1 | "Hoy la asignación de becas y ayudas sociales genera desconfianza: no se sabe bien qué reglas se aplicaron, ni si se aplicaron igual para todos. Quien queda afuera no puede auditar por qué." | Slide del problema (caja negra). |
| **0:30–1:15** (Solución) | Expositor/a 1 | "VeriBeca permite que la institución escriba sus reglas en un lenguaje simple. El sistema las valida sin errores de tipos, las aplica automáticamente, una IA prioriza por vulnerabilidad, y cada decisión queda sellada en blockchain para que cualquiera la audite." | Diagrama de arquitectura → pasar a la UI. |
| **1:15–2:15** (Demo en vivo) | Expositor/a 2 | "Escribo la regla… la valido — el type-checker la aprueba. Cargo 100 postulantes. Evalúo: 24 elegibles, ordenados por score de vulnerabilidad. Y acá está el certificado: este hash quedó registrado en la testnet de Ethereum (Sepolia), verificable en el explorer." | UI Streamlit: cargar regla → validar (mostrar también un error de regla mal escrita) → subir CSV → Evaluar → abrir el link de la transacción en el explorer. |
| **2:15–2:40** (Cierre + consigna) | Expositor/a 2 | "En un solo flujo integramos lenguajes, sistemas de tipos, compiladores, blockchain e IA — las unidades de la materia. VeriBeca pasa de 'confíen en nosotros' a 'verifíquenlo ustedes mismos'. Gracias." | Slide de cierre con la tabla de cobertura + link al repo. |

## Tips de grabación
- Tener el backend (`uvicorn`) y el frontend (`streamlit`) ya levantados antes de grabar.
- Si la blockchain está configurada (`.env`), mostrar el link real al explorer; si no, mostrar
  el certificado de fallback y mencionar que con `.env` configurado va on-chain.
- Mostrar **un error de tipos** (p. ej. `SI carrera < 5 ENTONCES elegible`) para evidenciar el
  type-checker — es el corazón académico del proyecto.
- Mantener el ritmo: ensayar para no pasar de 3 minutos.
