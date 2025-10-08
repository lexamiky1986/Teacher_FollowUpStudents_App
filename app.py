import streamlit as st
import pandas as pd
from datetime import datetime
from ml_model import entrenar_modelo
from nlp_utils import analizar_observacion, generar_pdf_por_grado

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
            "Nombre", "Grado", "Desempeño Académico",
            "Disciplina", "Aspecto Emocional", "Observaciones Docente",
            "Última Actualización"
        ])
    return df

def guardar_datos(df):
    df.to_csv("data/students_dat
