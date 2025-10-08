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
    df.to_csv("data/students_data.csv", index=False)

df = cargar_datos()

# =========================================================
# 🧭 Menú lateral
# =========================================================
menu = st.sidebar.selectbox(
    "Menú Principal",
    [
        "📊 Ver Datos",
        "✏️ Actualizar o Agregar Estudiante",
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

    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Promedio Académico", round(df["Desempeño Académico"].astype(float).mean(), 2))
        col2.metric("Promedio Disciplina", round(df["Disciplina"].astype(float).mean(), 2))
        col3.metric("Promedio Emocional", round(df["Aspecto Emocional"].astype(float).mean(), 2))
    else:
        st.info("Aún no hay datos registrados.")

# =========================================================
# ✏️ Agregar o actualizar estudiante
# =========================================================
elif menu == "✏️ Actualizar o Agregar Estudiante":
    st.header("✏️ Actualizar o Agregar Estudiante")

    grados_existentes = sorted(df["Grado"].dropna().unique())
    grados_opciones = grados_existentes + ["Nuevo Grado"]
    grado = st.selectbox("Selecciona el grado o crea uno nuevo", grados_opciones)

    if grado == "Nuevo Grado":
        grado = st.text_input("Escribe el nuevo grado:")

    nombres_existentes = df["Nombre"].unique().tolist()
    nombre = st.text_input("Nombre del estudiante:")

    if nombre:
        existe = ((df["Grado"] == grado) & (df["Nombre"].str.lower() == nombre.lower())).any()

        if existe:
            st.subheader(f"📄 Editar datos de {nombre} ({grado})")
            estudiante = df[(df["Grado"] == grado) & (df["Nombre"].str.lower() == nombre.lower())].iloc[0]
        else:
            st.subheader(f"🆕 Registrar nuevo estudiante ({grado})")
            estudiante = {
                "Desempeño Académico": 3.0,
                "Disciplina": 5,
                "Aspecto Emocional": 5,
                "Observaciones Docente": ""
            }

        with st.form("form_estudiante"):
            nuevo_academico = st.slider("Desempeño Académico (1.0 - 5.0)", 1.0, 5.0, float(estudiante["Desempeño Académico"]))
            nueva_disciplina = st.slider("Disciplina (0 - 10)", 0, 10, int(estudiante["Disciplina"]))
            nuevo_emocional = st.slider("Aspecto Emocional (0 - 10)", 0, 10, int(estudiante["Aspecto Emocional"]))
            nuevas_observaciones = st.text_area("Observaciones Docente", value=estudiante["Observaciones Docente"])

            submit = st.form_submit_button("💾 Guardar Cambios")

            if submit:
                if existe:
                    idx = df[(df["Grado"] == grado) & (df["Nombre"].str.lower() == nombre.lower())].index[0]
                    df.loc[idx, "Desempeño Académico"] = nuevo_academico
                    df.loc[idx, "Disciplina"] = nueva_disciplina
                    df.loc[idx, "Aspecto Emocional"] = nuevo_emocional
                    df.loc[idx, "Observaciones Docente"] = nuevas_observaciones
                    df.loc[idx, "Última Actualización"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success(f"✅ Datos de {nombre} actualizados correctamente.")
                else:
                    nuevo = pd.DataFrame([{
                        "Nombre": nombre,
                        "Grado": grado,
                        "Desempeño Académico": nuevo_academico,
                        "Disciplina": nueva_disciplina,
                        "Aspecto Emocional": nuevo_emocional,
                        "Observaciones Docente": nuevas_observaciones,
                        "Última Actualización": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    df = pd.concat([df, nuevo], ignore_index=True)
                    st.success(f"🆕 Nuevo estudiante {nombre} agregado correctamente.")

                guardar_datos(df)

# =========================================================
# 🤖 Análisis con IA
# =========================================================
elif menu == "🤖 Análisis e IA":
    st.header("🤖 Análisis con Machine Learning y NLP")

    if not df.empty:
        df_ml, modelo = entrenar_modelo(df)
        st.dataframe(df_ml[["Nombre", "Grado", "Desempeño Académico", "Disciplina", "Aspecto Emocional", "Grupo"]])

        st.markdown("""
        **Interpretación de los grupos (clusters):**
        - `0`: Estudiantes de alto desempeño integral.  
        - `1`: Estudiantes en nivel medio o en transición.  
        - `2`: Estudiantes con riesgo académico, emocional o disciplinario.  
        """)

        st.subheader("🧠 Estrategias generadas con NLP:")
        nombre = st.selectbox("Selecciona un estudiante para analizar observaciones", df["Nombre"].unique())
        obs = df[df["Nombre"] == nombre]["Observaciones Docente"].values[0]
        tono, estrategia_doc, estrategia_psico = analizar_observacion(str(obs))

        st.info(f"**Observación:** {obs}")
        st.write(f"**Tono detectado:** {tono}")
        st.write(f"**Estrategia Docente:** {estrategia_doc}")
        st.write(f"**Estrategia Psico-Familiar:** {estrategia_psico}")

    else:
        st.warning("No hay datos para analizar. Agrega estudiantes primero.")

# =========================================================
# 📄 Generar PDF por grado
# =========================================================
elif menu == "📄 Generar Informe PDF por Grado":
    st.header("📄 Generar Informe Consolidado por Grado")

    if not df.empty:
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
    else:
        st.warning("No hay información disponible para generar informes.")
