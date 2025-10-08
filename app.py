import os
import pandas as pd
import streamlit as st
from datetime import datetime
from ml_model import entrenar_modelo, generar_estrategias

# Librerías para PDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(page_title="Seguimiento Docente con IA", layout="wide")
st.title("📘 Sistema Integral de Seguimiento Académico, Disciplinario y Emocional")

DATA_PATH = "data/students_data.csv"
COLUMNAS = [
    "ID Estudiante", "Nombre", "Grado",
    "Desempeño Académico", "Disciplina", "Aspecto Emocional", "Observaciones Docente"
]

# ---------------- FUNCIONES ----------------
@st.cache_data
def cargar_datos():
    carpeta = os.path.dirname(DATA_PATH)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    if not os.path.exists(DATA_PATH):
        pd.DataFrame(columns=COLUMNAS).to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
        return pd.DataFrame(columns=COLUMNAS)

    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
        for col in COLUMNAS:
            if col not in df.columns:
                df[col] = pd.NA
        return df[COLUMNAS]
    except Exception as e:
        print(f"[ERROR] No se pudo leer {DATA_PATH}: {e}")
        return pd.DataFrame(columns=COLUMNAS)


def guardar_datos(df):
    carpeta = os.path.dirname(DATA_PATH)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")


def generar_pdf_por_grado(df, grado):
    """Genera un PDF con la información de un grado completo"""
    fecha = datetime.now().strftime("%d-%m-%Y")
    archivo_pdf = f"reporte_{grado}_{fecha}.pdf"

    doc = SimpleDocTemplate(
        archivo_pdf,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=50,
        bottomMargin=30
    )
    styles = getSampleStyleSheet()
    story = []

    # Portada
    story.append(Paragraph(f"<b>INFORME GENERAL - GRADO {grado}</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Fecha de generación: {fecha}", styles["Normal"]))
    story.append(Spacer(1, 24))

    column
