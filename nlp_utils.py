import spacy
from textblob import TextBlob
from fpdf import FPDF

nlp = spacy.load("en_core_web_sm")

def analizar_observacion(texto):
    if not texto or not isinstance(texto, str):
        return {"sentimiento": "Neutral", "polaridad": 0.0, "keywords": []}

    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    sentimiento = "Positivo" if polaridad > 0.1 else "Negativo" if polaridad < -0.1 else "Neutral"

    doc = nlp(texto)
    keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "ADJ"] and not token.is_stop]

    return {
        "sentimiento": sentimiento,
        "polaridad": round(polaridad, 3),
        "keywords": keywords[:10]
    }

def generar_pdf_por_grado(df, grado, output_path="informe_grado.pdf"):
    df_grado = df[df["Grado"] == grado]
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Informe de Seguimiento - Grado {grado}", ln=True, align="C")
    pdf.set_font("Arial", "", 12)

    for _, row in df_grado.iterrows():
        pdf.ln(8)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Estudiante: {row['Nombre']} (ID: {row['ID']})", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, f"Desempeño Académico: {row['Desempeño Académico']}")
        pdf.multi_cell(0, 8, f"Disciplina: {row['Disciplina']}")
        pdf.multi_cell(0, 8, f"Aspecto Emocional: {row['Aspecto Emocional']}")
        pdf.multi_cell(0, 8, f"Observaciones Docente: {row['Observaciones Docente']}")

        analisis = analizar_observacion(row["Observaciones Docente"])
        pdf.multi_cell(0, 8, f"Sentimiento: {analisis['sentimiento']} (Polaridad: {analisis['polaridad']})")
        pdf.multi_cell(0, 8, f"Palabras clave: {', '.join(analisis['keywords'])}")
        pdf.multi_cell(0, 8, f"Última Actualización: {row['Última Actualización']}")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.output(output_path)
    return output_path
