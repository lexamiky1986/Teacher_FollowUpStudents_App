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

    columnas = [
        "ID Estudiante", "Nombre", "Desempeño Académico", "Disciplina",
        "Aspecto Emocional", "Observaciones Docente",
        "Estrategia Docente", "Estrategia Psicoorientación", "Estrategia Familiar"
    ]

    data_table = [columnas]
    for _, row in df.iterrows():
        fila = [
            row["ID Estudiante"],
            row["Nombre"],
            f"{row['Desempeño Académico']:.1f}",
            row["Disciplina"],
            row["Aspecto Emocional"],
            row["Observaciones Docente"],
            row.get("Estrategia Docente", ""),
            row.get("Estrategia Psicoorientación", ""),
            row.get("Estrategia Familiar", "")
        ]
        data_table.append(fila)

    table = Table(data_table, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#cce5ff")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))
    story.append(table)
    doc.build(story)

    return archivo_pdf


# ---------------- INTERFAZ STREAMLIT ----------------
df = cargar_datos()

menu = st.sidebar.selectbox(
    "Menú principal",
    ["📊 Ver Datos", "➕ Agregar Observación", "🤖 Análisis IA / Estrategias", "🧾 Exportes"]
)

# --- 1. Ver datos ---
if menu == "📊 Ver Datos":
    st.subheader("📋 Listado de estudiantes")
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        st.write("📈 Promedio Académico:", round(df["Desempeño Académico"].mean(), 2))
        st.write("📈 Promedio Disciplinario:", round(df["Disciplina"].mean(), 2))
        st.write("📈 Promedio Emocional:", round(df["Aspecto Emocional"].mean(), 2))

# --- 2. Agregar observación ---
elif menu == "➕ Agregar Observación":
    st.subheader("✏️ Registrar seguimiento de estudiante")

    with st.form("nuevo_registro"):
        nombre = st.text_input("Nombre del estudiante")
        grado = st.selectbox("Grado", sorted(df["Grado"].unique()) if not df.empty else ["1°", "2°", "3°"])
        academico = st.slider("Desempeño académico (1.0 a 5.0)", 1.0, 5.0, 3.0)
        disciplina = st.slider("Disciplina (0 a 10)", 0, 10, 5)
        emocional = st.slider("Aspecto emocional (0 a 10)", 0, 10, 5)
        observacion = st.text_area("Observaciones del docente")
        submit = st.form_submit_button("Guardar")

        if submit:
            nuevo = {
                "ID Estudiante": int(datetime.now().timestamp()) % 10000 + 1200,
                "Nombre": nombre,
                "Grado": grado,
                "Desempeño Académico": academico,
                "Disciplina": disciplina,
                "Aspecto Emocional": emocional,
                "Observaciones Docente": observacion
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(df)
            st.success(f"✅ Registro agregado para {nombre}")

# --- 3. Análisis IA ---
elif menu == "🤖 Análisis IA / Estrategias":
    st.subheader("🤖 Análisis con Inteligencia Artificial")

    if df.empty:
        st.warning("No hay datos disponibles para analizar.")
    else:
        analyzed_df, model = entrenar_modelo()
        estrategias_df = generar_estrategias(analyzed_df)
        merged = analyzed_df.merge(estrategias_df, on="ID Estudiante", how="left")

        grado_sel = st.selectbox("Selecciona un grado:", sorted(merged["Grado"].unique()))
        df_grado = merged[merged["Grado"] == grado_sel]

        st.markdown(f"### 📚 Resultados para el grado {grado_sel}")

        st.bar_chart(
            df_grado.groupby("Perfil Clúster")[["Desempeño Académico", "Disciplina", "Aspecto Emocional"]].mean()
        )

        for cluster, grupo in df_grado.groupby("Perfil Clúster"):
            color = "🟢" if cluster == 0 else ("🟡" if cluster == 1 else "🔴")
            st.markdown(f"#### {color} Clúster {cluster}")
            st.dataframe(
                grupo[
                    [
                        "Nombre", "Desempeño Académico", "Disciplina", "Aspecto Emocional",
                        "Estrategia Docente", "Estrategia Psicoorientación", "Estrategia Familiar", "Observaciones Docente"
                    ]
                ],
                use_container_width=True,
            )

# --- 4. Exportes / PDF ---
elif menu == "🧾 Exportes":
    st.subheader("📄 Exportar reportes por grado")

    if df.empty:
        st.info("No hay datos para exportar.")
    else:
        analyzed_df, model = entrenar_modelo()
        estrategias_df = generar_estrategias(analyzed_df)
        merged = analyzed_df.merge(estrategias_df, on="ID Estudiante", how="left")

        grados = sorted(merged["Grado"].dropna().unique())
        grado_sel = st.selectbox("Selecciona un grado para generar el PDF:", grados)

        if st.button("🖨️ Generar PDF del grado seleccionado"):
            df_grado = merged[merged["Grado"] == grado_sel]
            archivo_pdf = generar_pdf_por_grado(df_grado, grado_sel)

            with open(archivo_pdf, "rb") as f:
                st.download_button(
                    label=f"⬇️ Descargar {archivo_pdf}",
                    data=f,
                    file_name=archivo_pdf,
                    mime="application/pdf"
                )

        st.markdown("---")
        st.download_button(
            "⬇️ Descargar CSV completo",
            df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            "students_data.csv",
            "text/csv"
        )
