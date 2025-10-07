import streamlit as st
import pandas as pd
from ml_model import entrenar_modelo, generar_estrategias
from datetime import datetime
import os

st.set_page_config(page_title="📘 Observador Docente", layout="wide")

st.title("📘 Seguimiento Académico, Disciplinario y Emocional")

# --- Cargar datos ---
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/datos_estudiantes.csv")

def guardar_datos(df):
    df.to_csv("data/datos_estudiantes.csv", index=False, encoding="utf-8-sig")

df = cargar_datos()

# --- Menú lateral ---
menu = st.sidebar.selectbox(
    "Menú Principal",
    ["📊 Ver Datos", "➕ Agregar Observación", "🤖 IA / Análisis"]
)

# --- Ver datos ---
if menu == "📊 Ver Datos":
    st.subheader("Listado de Estudiantes")
    st.dataframe(df)

    st.metric("Promedio Académico", round(df["Desempeño Académico"].mean(), 2))
    st.metric("Promedio Disciplina", round(df["Disciplina"].mean(), 2))
    st.metric("Promedio Emocional", round(df["Aspecto Emocional"].mean(), 2))

# --- Agregar nueva observación ---
elif menu == "➕ Agregar Observación":
    st.subheader("Registrar nueva observación")

    with st.form("nueva_observacion"):
        nombre = st.text_input("Nombre del estudiante")
        grado = st.selectbox("Grado", sorted(df["Grado"].unique()))
        desempeño = st.slider("Desempeño Académico (1.0 a 5.0)", 1.0, 5.0, 3.0)
        disciplina = st.slider("Disciplina (0 a 10)", 0, 10, 5)
        emocional = st.slider("Aspecto Emocional (0 a 10)", 0, 10, 5)
        observacion = st.text_area("Observación del Docente")
        enviar = st.form_submit_button("Guardar")

        if enviar:
            nuevo = {
                "ID Estudiante": int(datetime.now().timestamp()) % 100000,
                "Nombre": nombre,
                "Grado": grado,
                "Desempeño Académico": desempeño,
                "Disciplina": disciplina,
                "Aspecto Emocional": emocional,
                "Observaciones Docente": observacion
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(df)
            st.success("✅ Registro guardado correctamente.")

# --- IA / Análisis ---
elif menu == "🤖 IA / Análisis":
    st.subheader("Análisis con Inteligencia Artificial")

    analyzed_df, model = entrenar_modelo()
    estrategias_df = generar_estrategias(analyzed_df)
    merged = analyzed_df.merge(estrategias_df, on="ID Estudiante")

    grado_sel = st.selectbox("Selecciona un grado:", sorted(merged["Grado"].unique()))
    df_grado = merged[merged["Grado"] == grado_sel]

    st.markdown(f"### 📚 Resultados para el grado {grado_sel}")
    st.bar_chart(df_grado.groupby("Perfil Clúster")[["Desempeño Académico", "Disciplina", "Aspecto Emocional"]].mean())

    for cluster, grupo in df_grado.groupby("Perfil Clúster"):
        color = "🟢" if cluster == 0 else ("🟡" if cluster == 1 else "🔴")
        st.markdown(f"#### {color} Clúster {cluster}")
        st.dataframe(grupo[["Nombre", "Desempeño Académico", "Disciplina", "Aspecto Emocional", "Estrategia Docente", "Estrategia Psicoorientación", "Estrategia Familiar"]])
