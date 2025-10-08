from textblob import TextBlob
from fpdf import FPDF
import random
import pandas as pd

# =========================================================
# 🔹 1. Análisis individual de observaciones docentes
# =========================================================
def analizar_observacion(texto):
    """
    Analiza una observación de texto (docente) y devuelve:
      - Tono: Positivo, Negativo o Neutro
      - Estrategia Docente sugerida
      - Estrategia Psico-Familiar sugerida
    """

    if not isinstance(texto, str) or texto.strip() == "":
        return "Neutro", "Reforzar seguimiento académico general", "Comunicación básica con familia"

    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity

    # Clasificación de tono
    if polaridad > 0.2:
        tono = "Positivo"
    elif polaridad < -0.2:
        tono = "Negativo"
    else:
        tono = "Neutro"

    texto_lower = texto.lower()

    estrategias_docente = []
    estrategias_psico = []

    # 🔹 Análisis por palabras clave
    if any(p in texto_lower for p in ["desmotivado", "triste", "ansioso", "nervioso", "estresado"]):
        estrategias_docente.append("Apoyar desde tutoría y reforzar autoestima.")
        estrategias_psico.append("Reunión con orientador y familia para acompañamiento emocional.")

    if any(p in texto_lower for p in ["agresivo", "indisciplinado", "conflicto", "pelea"]):
        estrategias_docente.append("Aplicar pautas de manejo conductual y diálogo empático.")
        estrategias_psico.append("Orientar a los padres sobre límites y rutinas de apoyo.")

    if any(p in texto_lower for p in ["participativo", "motivado", "responsable", "líder"]):
        estrategias_docente.append("Reconocer su liderazgo y promover tutoría entre pares.")
        estrategias_psico.append("Mantener comunicación positiva con familia sobre avances.")

    if any(p in texto_lower for p in ["rendimiento", "bajo", "nota", "dificultad", "deficiente"]):
        estrategias_docente.append("Implementar plan de refuerzo académico personalizado.")
        estrategias_psico.append("Contactar familia para establecer hábitos de estudio.")

    # 🔹 Si no hay palabras clave, decidir según tono
    if not estrategias_docente:
        if tono == "Positivo":
            estrategias_docente.append("Potenciar fortalezas y promover nuevos retos académicos.")
            estrategias_psico.append("Retroalimentar positivamente a la familia.")
        elif tono == "Negativo":
            estrategias_docente.append("Realizar seguimiento individual y plan de mejora.")
            estrategias_psico.append("Citar familia para apoyo emocional y académico.")
        else:
            estrategias_docente.append("Observar evolución y mantener comunicación regular.")
            estrategias_psico.append("Orientar familia sobre apoyo cotidiano.")

    return tono, random.choice(estrategias_docente), random.choice(estrategias_psico)


# =========================================================
# 🔹 2. Generar texto de análisis resumido por grado
# =========================================================
def generar_texto_informe_por_grado(df, grado):
    """
    Devuelve texto de resumen con métricas, tono promedio
    y estrategias predominantes para un grado específico.
    """
    df_grado = df[df["Grado"] == grado]

    if df_grado.empty:
        return f"No hay información disponible para el grado {grado}."

    promedio_academico = round(df_grado["Desempeño Académico"].mean(), 2)
    promedio_disciplina = round(df_grado["Disciplina"].mean(), 2)
    promedio_emocional = round(df_grado["Aspecto Emocional"].mean(), 2)

    tonos, estrategias_doc, estrategias_psico = [], [], []
    for _, fila in df_grado.iterrows():
        tono, e_doc, e_psico = analizar_observacion(str(fila["Observaciones Docente"]))
        tonos.append(tono)
        estrategias_doc.append(e_doc)
        estrategias_psico.append(e_psico)

    df_grado = df_grado.copy()
    df_grado["Tono"] = tonos
    df_grado["Estrategia Docente"] = estrategias_doc
    df_grado["Estrategia Psico-Familiar"] = estrategias_psico

    tono_predominante = df_grado["Tono"].mode()[0]
    estrategia_doc_pred = df_grado["Estrategia Docente"].mode()[0]
    estrategia_psico_pred = df_grado["Estrategia Psico-Familiar"].mode()[0]

    texto = (
        f"📘 Informe general del grado {grado}\n\n"
        f"Promedio académico: {promedio_academico}\n"
        f"Promedio disciplinario: {promedio_disciplina}\n"
        f"Promedio emocional: {promedio_emocional}\n\n"
        f"Tono emocional predominante: {tono_predominante}\n"
        f"Estrategia docente general: {estrategia_doc_pred}\n"
        f"Estrategia psico-familiar general: {estrategia_psico_pred}\n"
    )

    return texto, df_grado


# =========================================================
# 🔹 3. Generar PDF visual por grado
# =========================================================
def generar_pdf_por_grado(df, grado, ruta_salida="informe_grado.pdf"):
    """
    Crea un informe PDF para un grado con resumen general
    y tabla de estrategias individuales.
    """
    resumen, df_grado = generar_texto_informe_por_grado(df, grado)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Informe del Grado {grado}", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, resumen)
    pdf.ln(5)

    # 🔹 Encabezado de tabla
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 8, "Nombre", 1, 0, "C")
    pdf.cell(25, 8, "Tono", 1, 0, "C")
    pdf.cell(60, 8, "Estrategia Docente", 1, 0, "C")
    pdf.cell(60, 8, "Estrategia Psico-Familiar", 1, 1, "C")

    pdf.set_font("Arial", "", 10)

    # 🔹 Filas
    for _, fila in df_grado.iterrows():
        pdf.cell(40, 8, fila["Nombre"][:20], 1, 0, "L")
        pdf.cell(25, 8, fila["Tono"], 1, 0, "C")
        pdf.cell(60, 8, fila["Estrategia Docente"][:40], 1, 0, "L")
        pdf.cell(60, 8, fila["Estrategia Psico-Familiar"][:40], 1, 1, "L")

    pdf.output(ruta_salida)
    return ruta_salida
