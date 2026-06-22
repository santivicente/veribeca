# Guion de la DEMO (la parte del medio del video)

**Estructura final del video:**
`[Compañero: intro/venta]  →  [DEMO: tu pantalla + tu voz]  →  [Compañero: cierre]`

Esta parte la grabás y narrás vos. Dura **~75-90 segundos**. Mostrás la app + Etherscan
mientras leés/decís el texto de abajo.

> Antes de grabar: app levantada en http://localhost:8501 y la transacción de Etherscan
> abierta en otra pestaña. Grabá la pantalla con Xbox Game Bar (Win+G), ShareX u OBS.

---

## Guion (texto a narrar + qué mostrar)

| # | Lo que decís (voz) | Lo que mostrás / hacés en pantalla |
|---|---|---|
| 1 | "Veamos VeriBeca funcionando." | La app abierta (localhost:8501) |
| 2 | "La institución define su criterio en un lenguaje simple. Por ejemplo: si el ingreso familiar es menor a 300 mil y el promedio es 7 o más, la persona es elegible." | Señalás la regla ya escrita en el recuadro |
| 3 | "El sistema valida la regla antes de usarla." | Apretás **Validar y cargar regla** → aparece el ✓ verde |
| 4 | "¿Y si la regla está mal escrita? Si intento comparar la carrera con un número, lo detecta y lo rechaza, antes de aplicarla. Así ningún error perjudica a un postulante." | Borrás y escribís `SI carrera < 5 ENTONCES elegible` → **Validar** → se ve el error de tipos |
| 5 | "Volvemos a la regla correcta y cargamos a los postulantes: en este caso, cien." | Volvés a poner la regla buena (validar) → subís `data\postulantes.csv` → **Cargar postulantes** |
| 6 | "Evaluamos. En segundos, el sistema aplica la regla a todos por igual, y una inteligencia artificial ordena a los elegibles por nivel de necesidad: primero quien más lo requiere." | Apretás **Evaluar** → se ve el ranking de 24 elegibles |
| 7 | "Cada decisión genera un certificado con un código único e irrepetible." | Hacés clic en el **#1** del ranking → mostrás el hash del certificado |
| 8 | "Y ese certificado queda registrado en la blockchain. Acá lo vemos: es una transacción real, pública, que nadie puede alterar ni borrar." | Cambiás a la pestaña de **Etherscan** con la transacción real |
| 9 | "Así, cualquiera puede auditar cómo y por qué se tomó cada decisión." | Quedás un par de segundos en Etherscan; corte → empieza el cierre del compañero |

---

## Texto corrido (por si preferís leerlo de una)

> "Veamos VeriBeca funcionando. La institución define su criterio en un lenguaje simple: por
> ejemplo, si el ingreso familiar es menor a 300 mil y el promedio es 7 o más, la persona es
> elegible. El sistema valida la regla antes de usarla. ¿Y si está mal escrita? Si intento
> comparar la carrera con un número, lo detecta y lo rechaza antes de aplicarla, así ningún
> error perjudica a un postulante. Volvemos a la regla correcta y cargamos a los postulantes:
> en este caso, cien. Evaluamos: en segundos el sistema los aplica a todos por igual, y una
> inteligencia artificial ordena a los elegibles por nivel de necesidad. Cada decisión genera
> un certificado con un código único, que queda registrado en la blockchain: una transacción
> real, pública, que nadie puede alterar. Así, cualquiera puede auditar cómo y por qué se tomó
> cada decisión."

---

## Cómo lo unís todo (edición)

1. Poné el clip de **intro de tu compañero** al principio.
2. Pegá tu **grabación de la demo** (con tu voz) en el medio.
3. Cerrá con el clip de **cierre de tu compañero**.
4. Revisá que el total sea **≤ 3 minutos** y que las transiciones no corten frases.
5. Subí el video y pegá el link en el `README.md`.
