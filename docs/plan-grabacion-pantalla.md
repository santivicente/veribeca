# Plan de grabación de pantalla — Video demo VeriBeca

**Situación:** un integrante graba el audio/cámara hablando (sin pantalla). Otro integrante
graba las pantallas que acompañan. Después se juntan en el editor.

---

## Cómo combinar las dos cosas (el método)

1. **Conseguí primero el video del compañero hablando** (el que tiene la narración).
2. **Escuchalo y anotá en qué segundo dice cada parte** (problema, solución, demo, cierre).
3. **Grabá la pantalla** siguiendo el plan de abajo, sin apuro (grabá de más, después recortás).
4. **En el editor** (Clipchamp / CapCut):
   - Pista 1: el video del compañero (su voz manda el ritmo).
   - Pista 2 (encima): tus grabaciones de pantalla, que se ven en grande.
   - Opcional: la cara del compañero chiquita en una esquina (picture-in-picture).
5. **Cortás la pantalla para que coincida** con lo que se está diciendo en cada momento.

> Consejo: grabá la pantalla en 3 clips separados (slides / app / Etherscan). Es mucho más
> fácil de sincronizar que una sola toma larga.

---

## Antes de grabar (preparación)

- Cerrá pestañas y notificaciones (que no aparezca nada personal).
- Tené abierto y listo:
  - El **pitch** (`docs/VeriBeca-Pitch.pptx`) en modo presentación.
  - La **app** levantada en http://localhost:8501 (ver comando abajo).
  - Una pestaña con la **transacción en Etherscan** ya abierta.
- Comando para levantar la app:
  `\.venv\Scripts\python.exe -m uvicorn backend.main:app` (terminal 1)
  `\.venv\Scripts\python.exe -m streamlit run frontend/app.py` (terminal 2)

---

## Plan de pantallas, momento a momento (≈2:40)

| Tiempo | Lo que dice la narración | Qué mostrás en pantalla | Qué hacés |
|---|---|---|---|
| **0:00–0:10** | Presentación / título | **Slide 1** (título VeriBeca) | Pantalla quieta, 5-10 seg |
| **0:10–0:30** | El problema | **Slide 2** (El problema) | Pasás a la slide 2 |
| **0:30–1:00** | La solución (los 5 pasos) | **Slide 3** (La solución) | Mostrás los 5 pasos |
| **1:00–1:15** | Cómo está armado | **Slide 5** (Arquitectura) | Pasás a la slide de arquitectura |
| **1:15–1:30** | "Les muestro cómo funciona" | **La app** (localhost:8501) | Cambiás a la app. Mostrás la regla ya escrita |
| **1:30–1:40** | "El sistema valida la regla" | App | Apretás **Validar** → sale el ✓ verde. Después escribís una regla MAL (ej: `carrera < 5`) y validás → mostrás el error de tipos |
| **1:40–1:55** | "Cargamos los postulantes" | App | Subís `data\postulantes.csv` → **Cargar** (dice "100 cargados") |
| **1:55–2:10** | "Evaluamos y prioriza por necesidad" | App | Apretás **Evaluar** → mostrás el ranking. Abrís el #1 y mostrás el certificado/hash |
| **2:10–2:20** | "...queda sellado en blockchain" | **Etherscan** (la tx real) | Cambiás a la pestaña de Etherscan con la transacción |
| **2:20–2:30** | Cómo cumple la materia | **Slide 6** (tabla de la consigna) | Volvés al pitch, slide 6 |
| **2:30–2:40** | Cierre | **Slide 10** (cierre) | Terminás en la slide de cierre |

> Los tiempos son una guía. Ajustalos a lo que realmente dura el audio de tu compañero.

---

## La demo en la app (los clics exactos, en orden)

1. La regla ya viene escrita: `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`.
   Apretás **"Validar y cargar regla"** → aparece "✅ Regla válida y cargada".
2. (Opcional pero recomendado) Borrás y escribís `SI carrera < 5 ENTONCES elegible`, validás →
   aparece el **error del type-checker**. Volvés a poner la regla buena y validás de nuevo.
3. En "Cargá los postulantes" subís `data\postulantes.csv` → **"Cargar postulantes"**.
4. Apretás **"Evaluar"** → se ve el ranking de 24 elegibles ordenados por score.
5. Hacés clic en el **#1** para desplegar y mostrar su certificado (hash).

---

## Tips de edición (para que quede pro)

- Poné un **título arriba** en cada bloque (ej: "1. El problema", "Demo en vivo").
- Cuando muestres Etherscan, **resaltá** el hash o poné un cartelito "Transacción real verificable".
- Música de fondo suave y bajita (que no tape la voz).
- Cortá los silencios y los momentos en que la pantalla "piensa".
- Al final, **fijate que no se pase de 3 minutos.**

---

## Checklist antes de subir

- [ ] El video dura ≤ 3 minutos.
- [ ] Se entiende el audio y se ven bien las pantallas.
- [ ] Aparece la demo funcionando + la transacción real en Etherscan.
- [ ] Subido (YouTube/Drive) y el **link pegado en el README**.
