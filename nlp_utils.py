import random
import re
from textblob import TextBlob

# =============================
# 🔍 ANALISIS DE TEXTO Y SENTIMIENTO
# =============================

def analizar_sentimiento(texto: str) -> str:
    """Analiza el tono emocional de un texto: positivo, negativo o neutro."""
    if not texto or len(texto.strip()) == 0:
        return "neutro"

    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity

    if polaridad > 0.1:
        return "positivo"
    elif polaridad < -0.1:
        return "negativo"
    else:
        return "neutro"


# =============================
# 🧩 DETECCIÓN DE TEMAS CLAVE
# =============================

def detectar_temas(texto: str):
    """Detecta temas relevantes en las observaciones del docente."""
    texto = texto.lower()
    temas = set()

    palabras_clave = {
        "ansiedad": ["ansioso", "estres", "nervioso", "inseguro", "presion"],
        "liderazgo": ["lider", "guia", "influencia", "motiva", "apoya"],
        "conflicto": ["pelea", "discusion", "conflicto", "agresivo", "intolerante"],
        "bajo_rendimiento": ["bajo", "deficiente", "malo", "poca", "insuficiente"],
        "excelente": ["excelente", "destaca]()
