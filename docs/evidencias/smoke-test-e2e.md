# Evidencia — Prueba end-to-end del MVP

Ejecución real del flujo completo (backend FastAPI + DSL + IA + registro de certificado)
sobre el dataset sintético de 100 postulantes (`data/postulantes.csv`).

**Regla aplicada:**
```
SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible
```

**Salida del backend:**
```
reglas: {'ok': True, 'mensaje': 'Regla valida y cargada'}
postulantes: {'ok': True, 'cantidad': 100}
elegibles: 24 | no elegibles: 76
  TOP 51 Postulante 51 score 0.8623 cert fallback 0x4acdd660c1322911...
  TOP 90 Postulante 90 score 0.8258 cert fallback 0xed2fdcdddb38a63c...
  TOP  9 Postulante 9  score 0.7608 cert fallback 0x853d563c810c7601...
```

**Qué demuestra:**
- El DSL valida la regla (type-checker) y el intérprete clasifica a los 100 postulantes
  en elegibles / no elegibles.
- La IA ordena a los 24 elegibles por score de vulnerabilidad (descendente).
- Por cada decisión se genera un hash de auditoría. En esta corrida el modo es `fallback`
  (local) porque aún no se desplegó el contrato; al configurar `.env` con un contrato en
  Ethereum Sepolia, el modo pasa a `onchain` con su transacción verificable.

**Suite de tests:** `27 passed` (DSL 20 + IA 3 + backend 2 + contracts 2).
