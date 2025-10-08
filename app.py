import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Importar módulos personalizados
from modules.ml_model import entrenar_modelo
from modules.nlp_utils import analizar_observacion, generar_pdf_por_grado

# Configuración de la aplicación
st.set_page_config(page_title="📘 Seguimiento Docente Integral", layout="wide")

# Ruta del archivo de datos
DATA_PATH = "data/students_data.csv"

# Función para cargar datos
@st.cache_data(ttl=300)
def cargar_datos():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    else:
        return pd.DataFrame(columns=[
            "ID", "Nombre", "Grado", "Desempeño Académico",
            "Disciplina", "Aspecto Emocional", "Observaciones Docente",
            "Última Actualización"
        ])

# Función para guardar datos
def guardar_datos(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")

# Cargar datos al iniciar
df = cargar_datos()

# Menú lateral
menu = st.sidebar.selectbox("Menú Principal", [
    "📊 Ver Datos",
    "✏️ Agregar / Actualizar Estudiante",
    "🤖 Análisis e IA",
    "📄 Generar Informe PDF por Grado"
])

# 📊 Ver Datos
if menu == "📊 Ver Datos":
    st.header("📚 Seguimiento Académico, Disciplinario y Emocional")
    st.dataframe(df, use_container_width=True)

# ✏️ Agregar / Actualizar Estudiante
elif menu == "✏️ Agregar / Actualizar Estudiante":
    st.header("✏️ Registro de Estudiante")
    with st.form("form_estudiante"):
        col1, col2 = st.columns(2)
        with col1:
            id_est = st.text_input("ID del Estudiante")
            nombre = st.text_input("Nombre Completo")
            grado = st.selectbox("Grado", ["1", "2", "3", "4", "5", "6"])
        with col2:
            rendimiento = st.selectbox("Desempeño Académico", ["Excelente", "Bueno", "Regular", "Deficiente"])
            disciplina = st.selectbox("Disciplina", ["Ejemplar", "Adecuada", "Con Conflictos"])
            emocional = st.selectbox("Aspecto Emocional", ["Estable", "Inestable", "Ansioso", "Motivado"])
        observaciones = st.text_area("Observaciones del Docente")
        enviar = st.form_submit_button("Guardar")

    if enviar:
        nueva_fila = {
            "ID": id_est,
            "Nombre": nombre,
            "Grado": grado,
            "Desempeño Académico": rendimiento,
            "Disciplina": disciplina,
            "Aspecto Emocional": emocional,
            "Observaciones Docente": observaciones,
            "Última Actualización": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = df[df["ID"] != id_est]
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        guardar_datos(df)
        st.success("✅ Estudiante guardado correctamente.")

# 🤖 Análisis e IA
elif menu == "🤖 Análisis e IA":
    st.header("🤖 Análisis de Observaciones Docentes")
    texto = st.text_area("Ingrese una observación para analizar")
    if st.button("Analizar"):
        resultado = analizar_observacion(texto)
        st.write("🔍 Resultado del análisis:")
        st.json(resultado)

    st.divider()
    st.subheader("📈 Entrenamiento de Modelo")
    if st.button("Entrenar modelo con datos actuales"):
        modelo, reporte = entrenar_modelo(df)
        st.success("✅ Modelo entrenado correctamente.")
        st.text("📊 Reporte de clasificación:")
        st.text(reporte)

# 📄 Generar Informe PDF por Grado
elif menu == "📄 Generar Informe PDF por Grado":
    st.header("📄 Informe PDF por Grado")
    grado_seleccionado = st.selectbox("Seleccione el grado", sorted(df["Grado"].unique()))
    if st.button("Generar PDF"):
        ruta_pdf = generar_pdf_por_grado(df, grado_seleccionado)
        with open(ruta_pdf, "rb") as f:
            st.download_button("📥 Descargar Informe PDF", f, file_name=os.path.basename(ruta_pdf), mime="application/pdf")
