import streamlit as st
import pandas as pd
from datetime import datetime
from ml_model import entrenar_modelo
from nlp_utils import analizar_observacion, generar_pdf_por_grado
import random

st.set_page_config(page_title="📘 Seguimiento Docente Integral", layout="wide")

# =========================================================
# 📂 Cargar y guardar datos
# =========================================================
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("data/students_data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "ID", "Nombre", "Grado", "Desempeño Académico",
            "Disciplina", "Aspecto Emocional", "Observaciones Docente",
            "Última Actualización"
        ])
    return df

def guardar_datos(df):
    df.to_csv("data/students_data.csv", index=False, encoding="utf-8-sig")

df = cargar_datos()

# =========================================================
# 🧭 Menú lateral
# =========================================================
menu = st.sidebar.selectbox(
    "Menú Principal",
    [
        "📊 Ver Datos",
        "✏️ Agregar / Actualizar Estudiante",
        "🤖 Análisis e IA",
        "📄 Generar Informe PDF por Grado"
    ]
)

# =========================================================
# 📊 Ver Datos
# =========================================================
if menu == "📊 Ver Datos":
    st.header("📚 Seguimiento Académico, Disciplinario y Emocional")
