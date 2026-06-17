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
st.caption("Reglas en un DSL tipado · IA que prioriza por vulnerabilidad · auditoría en blockchain")

st.header("1. Definí la regla de elegibilidad")
st.markdown(
    "Ejemplo de sintaxis: `SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible`  \n"
    "Operadores: `< <= > >= == !=` · Conectores: `Y`, `O`, `NO` · Paréntesis: `( )`"
)
regla = st.text_area(
    "Regla (DSL)",
    "SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible",
)
if st.button("Validar y cargar regla"):
    try:
        r = requests.post(f"{API}/reglas", json={"texto": regla, "schema_vars": SCHEMA})
        if r.status_code == 200:
            st.success("✅ Regla válida y cargada (pasó el type-checker)")
        else:
            st.error(f"❌ {r.json()['detail']}")
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar al backend. ¿Está corriendo `uvicorn backend.main:app`?")

st.header("2. Cargá los postulantes (CSV)")
st.caption("Podés usar el dataset de ejemplo en `data/postulantes.csv`.")
archivo = st.file_uploader("CSV de postulantes", type="csv")
if archivo is not None:
    df = pd.read_csv(archivo)
    if "trabaja" in df.columns:
        df["trabaja"] = df["trabaja"].astype(str).str.lower().map({"true": True, "false": False})
    st.dataframe(df.head())
    if st.button("Cargar postulantes"):
        r = requests.post(f"{API}/postulantes", json={"postulantes": df.to_dict("records")})
        st.success(f"✅ {r.json()['cantidad']} postulantes cargados")

st.header("3. Evaluar y priorizar")
if st.button("Evaluar"):
    try:
        r = requests.post(f"{API}/evaluar", json={})
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar al backend.")
        st.stop()
    if r.status_code != 200:
        st.error(f"❌ {r.json()['detail']}")
        st.stop()
    data = r.json()

    st.subheader(f"Ranking de elegibles por vulnerabilidad ({len(data['ranking'])})")
    for i, p in enumerate(data["ranking"], 1):
        cert = p["certificado"]
        nombre = p.get("nombre", p.get("id"))
        with st.expander(f"#{i} — {nombre} · score {p['score']}"):
            st.write({k: v for k, v in p.items() if k != "certificado"})
            if cert["modo"] == "onchain":
                st.markdown(f"🔗 [Ver transacción en Sepolia](https://sepolia.etherscan.io/tx/{cert['tx']})")
            else:
                st.info(f"Certificado de auditoría (fallback local):\n\n`{cert['hash']}`")

    st.subheader(f"No elegibles ({len(data['no_elegibles'])})")
    st.write([p.get("nombre", p.get("id")) for p in data["no_elegibles"]])
