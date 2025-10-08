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
    polar
