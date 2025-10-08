import spacy
from transformers import pipeline
import re

# Cargar modelo en español
try:
    nlp_spacy = spacy.load("es_core_news_sm")
except:
    import os
    os.system("python -m spacy download es_core_news_sm")
    nlp_spacy = spacy.load("es_core_news_sm")

# Modelo de sentimientos (multilingüe)
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analizar_observacion(observacion):
    """Analiza observaciones y genera estrategias docentes"""
    if not isinstance(observacion, str) or observacion.strip() == "":
        return "neutral", "Sin observaciones.", "Sin estrategias sugeridas."

    texto = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]", "", observacion).strip()
    doc = nlp_spacy(texto)
    sentimiento = sentiment_model(texto[:512])[0]
    label = sentimiento["label"].lower()

    if "1" in label or "2" in label:
        tono = "negativo"
    elif "4" in label or "5" in label:
        tono = "positivo"
    else:
        tono = "neutral"

    if tono == "negativo":
        estrategia_docente = "Reforzar acompañamiento académico y motivacional con tutorías."
        estrategia_psico = "Revisar factores emocionales. Coordinar cita con orientación escolar. Contactar familia."
    elif tono == "positivo":
        estrategia_docente = "Continuar fortaleciendo habilidades y reconocer avances."
        estrategia_psico = "Reforzar autoestima y liderazgo. Mantener comunicación familiar positiva."
    else:
        estrategia_docente = "Monitorear progreso y registrar observaciones semanales."
        estrategia_psico = "Observar comportamiento en próximas semanas. Comunicación abierta con la familia."

    return tono, estrategia_docente, estrategia_psico
