# app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from ml_model import entrenar_modelo, generar_estrategias
from generate_data import generar_datos_estudiantes

# Config
st.set_page_config(page_title="📘 Observador Docente", layout="wide")
DATA_PATH = os.path.join("data", "students_data.csv")
COLUMNAS = [
    "ID Estudiante","Nombre","Grado",
    "Desempeño Académico","Disciplina","Aspecto Emocional","Observaciones Docente"
]

# --- Helpers robustos de carga/guardado ---
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
        st.error(f"Error leyendo {DATA_PATH}: {e}")
        return pd.DataFrame(columns=COLUMNAS)

def guardar_datos(df):
    carpeta = os.path.dirname(DATA_PATH)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")

# --- UI ---
st.title("📘 Observador Docente — Seguimiento Académico / Disciplinario / Emocional")

# Cargar datos
df = cargar_datos()

# Menú
menu = st.sidebar.selectbox("Menú", [
    "📊 Ver Datos",
    "➕ Agregar Observación",
    "🎲 Generar Datos de Prueba",
    "🤖 IA / Análisis",
    "🧾 Exportes"
])

# --- Ver datos ---
if menu == "📊 Ver Datos":
    st.subheader("Listado de estudiantes")
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Promedio Académico", round(df["Desempeño Académico"].mean(), 2))
        col2.metric("Promedio Disciplina", round(df["Disciplina"].mean(), 2))
        col3.metric("Promedio Emocional", round(df["Aspecto Emocional"].mean(), 2))

# --- Agregar observación ---
elif menu == "➕ Agregar Observación":
    st.subheader("Registrar nueva observación")
    with st.form("nueva_observacion"):
        nombre = st.text_input("Nombre del estudiante")
        grado = st.selectbox("Grado", sorted(df["Grado"].dropna().unique()) if not df.empty else ["6°","7°","8°","9°","10°","11°"])
        desempeño = st.slider("Desempeño Académico (1.0 a 5.0)", 1.0, 5.0, 3.0)
        disciplina = st.slider("Disciplina (0 a 10)", 0, 10, 5)
        emocional = st.slider("Aspecto Emocional (0 a 10)", 0, 10, 5)
        observacion = st.text_area("Observación del docente")
        enviar = st.form_submit_button("Guardar")

        if enviar:
            # Generar ID numérico sencillo (evitar colisiones rápidas)
            existing_ids = set(df["ID Estudiante"].dropna().astype(int).tolist()) if not df.empty else set()
            new_id = None
            # buscar un id disponible en rango 12001-13666
            for candidate in range(12001, 13667):
                if candidate not in existing_ids:
                    new_id = candidate
                    break
            if new_id is None:
                new_id = int(datetime.now().timestamp()) % 100000 + 20000

            nuevo = {
                "ID Estudiante": new_id,
                "Nombre": nombre,
                "Grado": grado,
                "Desempeño Académico": desempeño,
                "Disciplina": disciplina,
                "Aspecto Emocional": emocional,
                "Observaciones Docente": observacion
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(df)
            st.success("✅ Registro guardado correctamente.")
            st.experimental_rerun()

# --- Generar datos de prueba ---
elif menu == "🎲 Generar Datos de Prueba":
    st.subheader("Generar datos simulados coherentes (Faker)")
    n = st.number_input("Número de estudiantes a generar", min_value=1, max_value=1000, value=150)
    if st.button("Generar y guardar en CSV"):
        df_new = generar_datos_estudiantes(n)
        guardar_datos(df_new)
        st.success(f"✅ {n} estudiantes generados y guardados en '{DATA_PATH}'.")
        st.experimental_rerun()

# --- IA / Análisis ---
elif menu == "🤖 IA / Análisis":
    st.subheader("Análisis con ML y generación de estrategias")
    if df.empty:
        st.info("No hay datos. Genera o sube un CSV con estudiantes.")
    else:
        analyzed_df, model = entrenar_modelo()
        estrategias_df = generar_estrategias(analyzed_df)
        merged = analyzed_df.merge(estrategias_df, on="ID Estudiante", how="left")

        grados = sorted(merged["Grado"].dropna().unique())
        grado_sel = st.selectbox("Selecciona un grado:", grados)
        df_grado = merged[merged["Grado"] == grado_sel]

        st.markdown(f"### 📚 Resultados para el grado {grado_sel}")
        st.bar_chart(df_grado.groupby("Perfil Clúster")[["Desempeño Académico","Disciplina","Aspecto Emocional"]].mean())

        for cluster, grupo in df_grado.groupby("Perfil Clúster"):
            color = "🟢" if cluster == 0 else ("🟡" if cluster == 1 else "🔴")
            st.markdown(f"#### {color} Clúster {cluster}")
            st.dataframe(
                grupo[[
                    "ID Estudiante","Nombre","Desempeño Académico","Disciplina","Aspecto Emocional",
                    "Observaciones Docente","Estrategia Docente","Estrategia Psicoorientación","Estrategia Familiar"
                ]].sort_values(by="Desempeño Académico", ascending=False),
                use_container_width=True
            )

        st.download_button(
            "⬇️ Descargar resultados analizados (CSV)",
            merged.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            "resultados_analizados.csv",
            "text/csv"
        )

# --- Exportes / PDF básicos ---
elif menu == "🧾 Exportes":
    st.subheader("Exportes")
    if df.empty:
        st.info("No hay datos para exportar.")
    else:
        if st.button("Descargar CSV actual"):
            st.download_button(
                "Descargar CSV",
                df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
                "students_data.csv",
                "text/csv"
            )
        st.markdown("Para generar PDFs personalizados por estudiante o por grado puedes solicitar la función; puedo agregarla.")
