import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
from ml_model import entrenar_modelo
from nlp_utils import analizar_observacion
from fpdf import FPDF

# ==========================
# CONFIGURACIÓN GENERAL
# ==========================
st.set_page_config(page_title="Seguimiento Integral Docente", layout="wide")
st.title("📘 Sistema Integral de Seguimiento Académico, Disciplinario y Psicoemocional")

DATA_PATH = "data/students_data.csv"
COLUMNAS = [
    "ID Estudiante", "Nombre", "Grado",
    "Desempeño Académico", "Disciplina",
    "Aspecto Emocional", "Observaciones Docente"
]

# ==========================
# FUNCIONES DE DATOS
# ==========================
@st.cache_data
def cargar_datos():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_PATH):
        pd.DataFrame(columns=COLUMNAS).to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    return pd.read_csv(DATA_PATH, encoding="utf-8-sig")

def guardar_datos(df):
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")

df = cargar_datos()

# ==========================
# MENÚ LATERAL
# ==========================
menu = st.sidebar.selectbox("Menú principal", [
    "📋 Ver Datos",
    "➕ Agregar Observación",
    "🤖 Análisis con IA",
    "🧠 Estrategias con NLP",
    "📄 Generar PDF por Grado"
])

# ==========================
# 📋 VER DATOS
# ==========================
if menu == "📋 Ver Datos":
    st.subheader("Listado de estudiantes")
    st.dataframe(df, use_container_width=True)
    st.write("Promedio Académico:", round(df["Desempeño Académico"].mean(), 2))
    st.write("Promedio Disciplinario:", round(df["Disciplina"].mean(), 2))
    st.write("Promedio Emocional:", round(df["Aspecto Emocional"].mean(), 2))

# ==========================
# ➕ AGREGAR OBSERVACIÓN
# ==========================
elif menu == "➕ Agregar Observación":
    st.subheader("Registrar nueva observación")

    with st.form("nuevo_registro"):
        nombre = st.text_input("Nombre del estudiante")
        grado = st.text_input("Grado o curso")
        academico = st.slider("Desempeño Académico (1.0 a 5.0)", 1.0, 5.0, 3.0)
        disciplina = st.slider("Disciplina (0 a 10)", 0, 10, 5)
        emocional = st.slider("Aspecto Emocional (0 a 10)", 0, 10, 5)
        observacion = st.text_area("Observaciones del docente")
        enviar = st.form_submit_button("Guardar registro")

        if enviar:
            nuevo = {
                "ID Estudiante": np.random.randint(1200, 3666),
                "Nombre": nombre,
                "Grado": grado,
                "Desempeño Académico": academico,
                "Disciplina": disciplina,
                "Aspecto Emocional": emocional,
                "Observaciones Docente": observacion
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(df)
            st.success("✅ Registro guardado correctamente.")

# ==========================
# 🤖 ANÁLISIS CON IA
# ==========================
elif menu == "🤖 Análisis con IA":
    st.subheader("Análisis de Clústeres de Estudiantes")
    df, modelo = entrenar_modelo(df)
    st.dataframe(df)

    st.bar_chart(df.groupby("Grupo")[["Desempeño Académico", "Disciplina", "Aspecto Emocional"]].mean())

    grado_sel = st.selectbox("Seleccionar grado para ver sus grupos", sorted(df["Grado"].unique()))
    st.dataframe(df[df["Grado"] == grado_sel])

# ==========================
# 🧠 ESTRATEGIAS NLP
# ==========================
elif menu == "🧠 Estrategias con NLP":
    st.subheader("Análisis de Observaciones y Estrategias Personalizadas")

    resultados = []
    for _, row in df.iterrows():
        tono, est_doc, est_psico = analizar_observacion(row["Observaciones Docente"])
        resultados.append({
            "Nombre": row["Nombre"],
            "Grado": row["Grado"],
            "Tono": tono,
            "Estrategia Docente": est_doc,
            "Estrategia Psicoemocional y Familiar": est_psico
        })

    nlp_df = pd.DataFrame(resultados)
    st.dataframe(nlp_df, use_container_width=True)

    st.download_button(
        "⬇️ Descargar estrategias (CSV)",
        data=nlp_df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="estrategias_docentes.csv",
        mime="text/csv"
    )

# ==========================
# 📄 GENERAR PDF POR GRADO
# ==========================
elif menu == "📄 Generar PDF por Grado":
    st.subheader("Generar informe PDF por grado")

    grado_sel = st.selectbox("Seleccionar grado", sorted(df["Grado"].unique()))
    subset = df[df["Grado"] == grado_sel]

    if st.button("📘 Generar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, f"Informe del Grado {grado_sel}", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        for _, row in subset.iterrows():
            pdf.cell(0, 10, f"{row['Nombre']} - Académico: {row['Desempeño Académico']} | Disciplina: {row['Disciplina']} | Emocional: {row['Aspecto Emocional']}", ln=True)
            pdf.multi_cell(0, 8, f"Observación: {row['Observaciones Docente']}\n")
            pdf.ln(3)

        pdf_path = f"data/Informe_{grado_sel}.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar PDF",
                data=f,
                file_name=f"Informe_{grado_sel}.pdf",
                mime="application/pdf"
            )
        st.success(f"✅ Informe generado: {pdf_path}")
