import re

# ============================================
# 1️⃣ Intentar cargar spaCy en español
# ============================================
try:
    import spacy
    try:
        nlp_spacy = spacy.load("es_core_news_sm")
    except OSError:
        # Descarga automática solo si es posible
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
        nlp_spacy = spacy.load("es_core_news_sm")
except Exception as e:
    print(f"⚠️ spaCy no disponible: {e}")
    nlp_spacy = None

# ============================================
# 2️⃣ Intentar cargar modelo de sentimientos
# ============================================
try:
    from transformers import pipeline
    sentiment_model = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        use_auth_token=False
    )
    modelo_activo = "bert"
except Exception as e:
    print(f"⚠️ No se pudo cargar el modelo BERT. Se usará TextBlob. Error: {e}")
    from textblob import TextBlob
    sentiment_model = None
    modelo_activo = "textblob"

# ============================================
# 3️⃣ Función principal de análisis
# ============================================
def analizar_observacion(observacion: str):
    """
    Analiza una observación textual y devuelve:
    - tono general (positivo, negativo, neutral)
    - estrategia docente
    - estrategia psicosocial
    """

    if not isinstance(observacion, str) or observacion.strip() == "":
        return "neutral", "Sin observaciones registradas.", "Sin estrategias sugeridas."

    texto = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]", "", observacion).strip()

    # Procesamiento lingüístico (si spaCy está disponible)
    if nlp_spacy:
        doc = nlp_spacy(texto)
        tokens = [t.lemma_.lower() for t in doc if not t.is_stop]
        texto = " ".join(tokens)

    # Sentimiento
    if modelo_activo == "bert" and sentiment_model:
        sentimiento = sentiment_model(texto[:512])[0]
        label = sentimiento["label"].lower()
        if "1" in label or "2" in label:
            tono = "negativo"
        elif "4" in label or "5" in label:
            tono = "positivo"
        else:
            tono = "neutral"
    else:
        blob = TextBlob(texto)
        polarity = blob.sentiment.polarity
        if polarity < -0.1:
            tono = "negativo"
        elif polarity > 0.1:
            tono = "positivo"
        else:
            tono = "neutral"

    # Estrategias sugeridas
    if tono == "negativo":
        estrategia_docente = "Aplicar acompañamiento académico y emocional; reforzar motivación."
        estrategia_psico = "Contactar familia y coordinar apoyo con psicoorientación."
    elif tono == "positivo":
        estrategia_docente = "Reforzar fortalezas y fomentar liderazgo académico."
        estrategia_psico = "Mantener comunicación positiva con la familia."
    else:
        estrategia_docente = "Monitorear progreso; seguimiento quincenal."
        estrategia_psico = "Observar comportamiento y promover espacios de diálogo familiar."

    return tono, estrategia_docente, estrategia_psico
