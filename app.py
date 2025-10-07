import streamlit as st
import pandas as pd
from datetime import datetime
from ml_model import train_model
from nlp_module import analizar_observacion

st.set_page_config(page_title="Seguimiento Docente", layout="wide")

st.title("📚 Seguimiento Académico, Disciplinario y Emocional")

# --- Cargar datos ---
@st.cache_data
def load_data():
    return pd.read_csv("data/students_data.csv")

def save_data(df):
    df.to_csv("data/students_data.csv", index=False)

df = load_data()

# --- Menú lateral ---
menu = st.sidebar.selectbox("Menú", [
    "📊 Ver Datos",
    "➕ Agregar Observación",
    "🤖 IA / Análisis",
    "🧠 Análisis NLP y Estrategias"
])

# --- Ver datos ---
if menu == "📊 Ver Datos":
    st.subheader("Listado de estudiantes")
    st.dataframe(df)

    st.write("Promedio Académico:", round(df["academic_score"].mean(), 2))
    st.write("Promedio Disciplinario:", round(df["disciplinary_score"].mean(), 2))
    st.write("Promedio Emocional:", round(df["emotional_score"].mean(), 2))

# --- Agregar nueva observación ---
elif menu == "➕ Agregar Observación":
    st.subheader("Agregar información de seguimiento")

    with st.form("new_entry"):
        name = st.text_input("Nombre del estudiante")
        grade = st.selectbox("Grado", sorted(df["grade"].unique()) if not df.empty else ["6A", "6B", "7A", "7B", "8A"])
        academic = st.slider("Desempeño académico (1.0 a 5.0)", 1.0, 5.0, 3.0)
        disciplinary = st.slider("Disciplina (0 a 10)", 0, 10, 5)
        emotional = st.slider("Emocional / Psicosocial (0 a 10)", 0, 10, 5)
        observation = st.text_area("Observaciones")
        submit = st.form_submit_button("Guardar")

        if submit:
            new_row = {
                "student_id": datetime.now().timestamp(),
                "name": name,
                "grade": grade,
                "academic_score": academic,
                "disciplinary_score": disciplinary,
                "emotional_score": emotional,
                "teacher_observation": observation
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("✅ Registro guardado con éxito.")

# --- Análisis con IA ---
elif menu == "🤖 IA / Análisis":
    st.subheader("Análisis con Inteligencia Artificial")
    analyzed_df, model = train_model()

    st.markdown("""
    **Interpretación de los clústeres (agrupaciones):**
    - 🟢 `0`: Grupo de alto desempeño
    - 🟡 `1`: Grupo con riesgo medio
    - 🔴 `2`: Grupo que requiere seguimiento especial
    """)

    grados = sorted(analyzed_df["grade"].unique())
    grado_sel = st.selectbox("Selecciona un grado:", grados)
    df_grado = analyzed_df[analyzed_df["grade"] == grado_sel]

    st.write(f"**Promedio Académico ({grado_sel}):**", round(df_grado["academic_score"].mean(), 2))
    st.write(f"**Promedio Disciplinario:**", round(df_grado["disciplinary_score"].mean(), 2))
    st.write(f"**Promedio Emocional:**", round(df_grado["emotional_score"].mean(), 2))

    st.markdown("### 📋 Listado de estudiantes por clúster")
    for cluster, grupo in df_grado.groupby("profile_cluster"):
        color = "🟢" if cluster == 0 else ("🟡" if cluster == 1 else "🔴")
        st.markdown(f"#### {color} Cluster {cluster}")
        st.dataframe(
            grupo[["name", "academic_score", "disciplinary_score", "emotional_score", "teacher_observation"]]
            .sort_values(by="academic_score", ascending=False)
        )

    st.markdown("### 📊 Distribución de los clústeres por grado")
    st.bar_chart(df_grado.groupby("profile_cluster")[["academic_score", "disciplinary_score", "emotional_score"]].mean())

# --- Análisis NLP ---
elif menu == "🧠 Análisis NLP y Estrategias":
    st.subheader("Análisis de Observaciones y Estrategias de Intervención")

    if len(df) == 0:
        st.warning("No hay datos registrados aún.")
    else:
        selected_student = st.selectbox("Selecciona un estudiante:", df["name"].unique())
        student_data = df[df["name"] == selected_student].iloc[-1]

        st.markdown(f"**Grado:** {student_data['grade']}")
        st.markdown(f"**Última observación:** {student_data['teacher_observation']}")

        if st.button("Analizar con IA"):
            resultado = analizar_observacion(student_data["teacher_observation"])
            st.markdown("### 🔍 Resultado del análisis")
            st.write(f"**Sentimiento general:** {resultado['sentimiento']} ({resultado['categoria']})")

            st.markdown("### 🎓 Estrategia docente sugerida")
            st.info(resultado["estrategia_docente"])

            st.markdown("### 🧩 Recomendación de psicoorientación")
            st.warning(resultado["psicoorientacion"])

            st.markdown("### 🏠 Trabajo con la familia")
            st.success(resultado["trabajo_familia"])
