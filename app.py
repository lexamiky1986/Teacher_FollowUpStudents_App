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
    df = pd.read_csv("data/students_data.csv")
    return df

def guardar_datos(df):
    df.to_csv("data/students_data.csv", index=False)

df = cargar_datos()

# =========================================================
# 🧭 Menú lateral
# =========================================================
menu = st.sidebar.selectbox(
    "Menú Principal",
    [
        "📊 Ver Datos",
        "✏️ Actualizar Información de Estudiante",
        "🤖 Análisis e IA",
        "📄 Generar Informe PDF por Grado"
    ]
)

# =========================================================
# 📊 Ver datos
# =========================================================
if menu == "📊 Ver Datos":
    st.header("📚 Seguimiento Académico, Disciplinario y Emocional")
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio Académico", round(df["Desempeño Académico"].mean(), 2))
    col2.metric("Promedio Disciplina", round(df["Disciplina"].mean(), 2))
    col3.metric("Promedio Emocional", round(df["Aspecto Emocional"].mean(), 2))

# =========================================================
# ✏️ Actualizar información existente
# =========================================================
elif menu == "✏️ Actualizar Información de Estudiante":
    st.header("✏️ Actualizar datos de un estudiante existente")

    grado = st.selectbox("Selecciona el grado", sorted(df["Grado"].unique()))
    df_grado = df[df["Grado"] == grado]

    if not df_grado.empty:
        nombre = st.selectbox("Selecciona el estudiante", df_grado["Nombre"].unique())
        estudiante = df_grado[df_grado["Nombre"] == nombre].iloc[0]

        st.write("### Información actual del estudiante:")
        st.write(estudiante)

        with st.form("actualizar_estudiante"):
            nuevo_academico = st.slider(
                "Desempeño Académico (1.0 - 5.0)",
                1.0, 5.0,
                float(estudiante["Desempeño Académico"])
            )
            nueva_disciplina = st.slider(
                "Disciplina (0 - 10)",
                0, 10,
                int(estudiante["Disciplina"])
            )
            nuevo_emocional = st.slider(
                "Aspecto Emocional (0 - 10)",
                0, 10,
                int(estudiante["Aspecto Emocional"])
            )
            nuevas_observaciones = st.text_area(
                "Observaciones Docente",
                value=estudiante["Observaciones Docente"]
            )

            submit = st.form_submit_button("💾 Guardar Cambios")

            if submit:
                # Actualizar la fila correspondiente
                idx = df[(df["Grado"] == grado) & (df["Nombre"] == nombre)].index[0]
                df.loc[idx, "Desempeño Académico"] = nuevo_academico
                df.loc[idx, "Disciplina"] = nueva_disciplina
                df.loc[idx, "Aspecto Emocional"] = nuevo_emocional
                df.loc[idx, "Observaciones Docente"] = nuevas_observaciones
                df.loc[idx, "Última Actualización"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                guardar_datos(df)
                st.success(f"✅ Datos de {nombre} actualizados correctamente.")

    else:
        st.warning(f"No hay estudiantes registrados en el grado {grado}.")

# =========================================================
# 🤖 Análisis con IA
# =========================================================
elif menu == "🤖 Análisis e IA":
    st.header("🤖 Análisis con Machine Learning y NLP")

    df_ml, modelo = entrenar_modelo(df)
    st.dataframe(df_ml[["Nombre", "Grado", "Desempeño Académico", "Disciplina", "Aspecto Emocional", "Grupo"]])

    st.markdown("""
    **Interpretación de los grupos (clusters):**
    - `0`: Estudiantes de alto desempeño integral.  
    - `1`: Estudiantes en nivel medio o en transición.  
    - `2`: Estudiantes con riesgo académico, emocional o disciplinario.  
    """)

    # Análisis NLP breve
    st.subheader("🧠 Estrategias generadas con NLP:")
    nombre = st.selectbox("Selecciona un estudiante para analizar observaciones", df["Nombre"].unique())
    obs = df[df["Nombre"] == nombre]["Observaciones Docente"].values[0]
    tono, estrategia_doc, estrategia_psico = analizar_observacion(str(obs))

    st.info(f"**Observación:** {obs}")
    st.write(f"**Tono detectado:** {tono}")
    st.write(f"**Estrategia Docente:** {estrategia_doc}")
    st.write(f"**Estrategia Psico-Familiar:** {estrategia_psico}")

# =========================================================
# 📄 Generar PDF por grado
# =========================================================
elif menu == "📄 Generar Informe PDF por Grado":
    st.header("📄 Generar Informe Consolidado por Grado")

    grado = st.selectbox("Selecciona el grado", sorted(df["Grado"].unique()))
    if st.button("🖨️ Generar PDF"):
        ruta = f"informe_{grado}.pdf"
        ruta_pdf = generar_pdf_por_grado(df, grado, ruta)
        with open(ruta_pdf, "rb") as f:
            st.download_button(
                label="⬇️ Descargar Informe PDF",
                data=f,
                file_name=f"informe_{grado}.pdf",
                mime="application/pdf"
            )
        st.success(f"Informe generado exitosamente para el grado {grado}.")
