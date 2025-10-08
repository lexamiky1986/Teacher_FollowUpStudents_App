import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from ml_model import entrenar_modelo
from nlp_utils import analizar_observacion, generar_texto_informe_por_grado
from fpdf import FPDF

# ------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------
st.set_page_config(page_title="📘 Seguimiento Docente", layout="wide")
DATA_PATH = "data/students_data.csv"

# ------------------------------------------------------------
# FUNCIONES DE APOYO
# ------------------------------------------------------------
@st.cache_data
def cargar_datos():
    if not os.path.exists(DATA_PATH):
        st.warning("⚠️ No se encontró el archivo de datos. Se creará uno nuevo vacío.")
        df = pd.DataFrame(columns=[
            "ID Estudiante", "Nombre", "Grado",
            "Desempeño Académico", "Disciplina",
            "Aspecto Emocional", "Observaciones Docente"
        ])
        df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    return pd.read_csv(DATA_PATH, encoding="utf-8-sig")

def guardar_datos(df):
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")

# Generar PDF de informe por grado
def generar_pdf(grado, texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Informe del grado {grado}", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    for linea in texto.split("\n"):
        pdf.multi_cell(0, 8, linea)
    nombre_archivo = f"Informe_Grado_{grado}.pdf"
    ruta = os.path.join("data", nombre_archivo)
    pdf.output(ruta)
    return ruta

# ------------------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------------------
df = cargar_datos()

# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------
menu = st.sidebar.selectbox(
    "Menú principal",
    ["📋 Ver Datos", "➕ Agregar Observación", "🤖 Análisis e IA", "📄 Generar Informe por Grado"]
)

# ------------------------------------------------------------
# VISTA 1: VER DATOS
# ------------------------------------------------------------
if menu == "📋 Ver Datos":
    st.title("📋 Seguimiento general de estudiantes")
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio Académico", round(df["Desempeño Académico"].mean(), 2))
    col2.metric("Promedio Disciplina", round(df["Disciplina"].mean(), 2))
    col3.metric("Promedio Emocional", round(df["Aspecto Emocional"].mean(), 2))

# ------------------------------------------------------------
# VISTA 2: AGREGAR OBSERVACIÓN
# ------------------------------------------------------------
elif menu == "➕ Agregar Observación":
    st.title("➕ Agregar nueva observación del docente")

    with st.form("nuevo_registro"):
        nombre = st.text_input("Nombre del estudiante")
        grado = st.text_input("Grado o curso")
        academico = st.slider("Desempeño académico (1.0 a 5.0)", 1.0, 5.0, 3.0)
        disciplina = st.slider("Disciplina (0 a 10)", 0, 10, 5)
        emocional = st.slider("Aspecto emocional / psicosocial (0 a 10)", 0, 10, 5)
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
            st.success(f"✅ Registro guardado para {nombre} (Grado {grado})")

# ------------------------------------------------------------
# VISTA 3: ANÁLISIS E IA
# ------------------------------------------------------------
elif menu == "🤖 Análisis e IA":
    st.title("🤖 Análisis con Inteligencia Artificial")

    if df.empty:
        st.warning("No hay datos disponibles.")
        st.stop()

    # Entrenar modelo de agrupamiento (ML)
    df_analizado, modelo = entrenar_modelo(df)

    # Aplicar análisis NLP por observación
    estrategias_docente = []
    estrategias_psico = []
    tonos = []

    for _, fila in df_analizado.iterrows():
        tono, estrategia_doc, estrategia_psico = analizar_observacion(fila["Observaciones Docente"])
        tonos.append(tono)
        estrategias_docente.append(estrategia_doc)
        estrategias_psico.append(estrategia_psico)

    df_analizado["Tono Observación"] = tonos
    df_analizado["Estrategia Docente"] = estrategias_docente
    df_analizado["Estrategia Psico-Familiar"] = estrategias_psico

    st.subheader("Resultados del análisis combinado")
    st.dataframe(df_analizado, use_container_width=True)

    st.markdown("""
    ### Interpretación general:
    - **Clúster 0**: Alto desempeño, bajo riesgo.  
    - **Clúster 1**: Rendimiento medio, seguimiento moderado.  
    - **Clúster 2**: Riesgo académico o emocional, requiere apoyo.  
    """)

    # Métricas agrupadas por grado
    st.subheader("Promedios por grado")
    st.bar_chart(df_analizado.groupby("Grado")[["Desempeño Académico", "Disciplina", "Aspecto Emocional"]].mean())

    # Listado por clúster
    st.subheader("Listados de estudiantes por grupo")
    for cluster in sorted(df_analizado["Grupo"].unique()):
        st.markdown(f"### 🧩 Grupo {cluster}")
        st.dataframe(df_analizado[df_analizado["Grupo"] == cluster][
            ["Nombre", "Grado", "Desempeño Académico", "Disciplina", "Aspecto Emocional", "Tono Observación"]
        ])

# ------------------------------------------------------------
# VISTA 4: GENERAR INFORME PDF POR GRADO
# ------------------------------------------------------------
elif menu == "📄 Generar Informe por Grado":
    st.title("📄 Generar informe PDF por grado")

    grados = df["Grado"].dropna().unique().tolist()
    if not grados:
        st.warning("No hay grados registrados.")
        st.stop()

    grado_sel = st.selectbox("Selecciona el grado", grados)

    if st.button("Generar PDF"):
        texto = generar_texto_informe_por_grado(df, grado_sel)
        ruta_pdf = generar_pdf(grado_sel, texto)
        st.success(f"✅ Informe generado: {ruta_pdf}")
        with open(ruta_pdf, "rb") as f:
            st.download_button(
                label="⬇️ Descargar PDF",
                data=f,
                file_name=os.path.basename(ruta_pdf),
                mime="application/pdf"
            )
