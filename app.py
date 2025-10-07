import streamlit as st
import pandas as pd
from ml_model import train_model
from datetime import datetime

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
menu = st.sidebar.selectbox("Menú", ["📊 Ver Datos", "➕ Agregar Observación", "🤖 IA / Análisis"])

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
        grade = st.selectbox("Grado", sorted(df["grade"].unique()))
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

# --- Análisis IA ---
# --- Análisis IA ---
elif menu == "🤖 IA / Análisis":
    st.subheader("Análisis con Inteligencia Artificial")
    analyzed_df, model = train_model()

    st.markdown("""
    **Interpretación de los clústeres (agrupaciones):**
    - 🟢 `0`: Grupo de alto desempeño
    - 🟡 `1`: Grupo con riesgo medio
    - 🔴 `2`: Grupo que requiere seguimiento especial
    """)

    # Selector de grado
    grados = sorted(analyzed_df["grade"].unique())
    grado_seleccionado = st.selectbox("Selecciona un grado:", grados)

    # Filtrar por grado
    df_grado = analyzed_df[analyzed_df["grade"] == grado_seleccionado]

    # Mostrar métricas del grado
    st.write(f"**Promedio Académico ({grado_seleccionado}):**", round(df_grado["academic_score"].mean(), 2))
    st.write(f"**Promedio Disciplinario:**", round(df_grado["disciplinary_score"].mean(), 2))
    st.write(f"**Promedio Emocional:**", round(df_grado["emotional_score"].mean(), 2))

    # Mostrar los estudiantes por clúster
    st.markdown("### 📋 Listado de estudiantes por clúster")

    for cluster, grupo in df_grado.groupby("profile_cluster"):
        color = "🟢" if cluster == 0 else ("🟡" if cluster == 1 else "🔴")
        st.markdown(f"#### {color} Cluster {cluster}")
        st.dataframe(
            grupo[["name", "academic_score", "disciplinary_score", "emotional_score", "teacher_observation"]]
            .sort_values(by="academic_score", ascending=False)
        )

    # Mostrar gráfico resumen
    st.markdown("### 📊 Distribución de los clústeres por grado")
    st.bar_chart(df_grado.groupby("profile_cluster")[["academic_score", "disciplinary_score", "emotional_score"]].mean())
    st.subheader("Análisis con Inteligencia Artificial")
    analyzed_df, model = train_model()
    st.dataframe(analyzed_df)

    st.markdown("""
    **Interpretación de los clústeres (agrupaciones):**
    - `0`: Posible grupo de alto desempeño.
    - `1`: Grupo con riesgo medio.
    - `2`: Grupo que requiere seguimiento especial.
    """)

    st.bar_chart(analyzed_df.groupby("profile_cluster")[["academic_score", "disciplinary_score", "emotional_score"]].mean())
