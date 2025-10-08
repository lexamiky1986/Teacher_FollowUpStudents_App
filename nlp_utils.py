import re

# ============================================
# 1️⃣ Cargar spaCy en español (seguro)
# ============================================
try:
    import spacy
    try:
        nlp_spacy = spacy.load("es_core_news_sm")
    except OSError:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"], check=False)
        nlp_spacy = spacy.load("es_core_news_sm")
except Exception as e:
    print(f"⚠️ spaCy no disponible: {e}")
    nlp_spacy = None

# ============================================
# 2️⃣ Cargar modelo de sentimientos (transformers o TextBlob)
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
    print(f"⚠️ No se pudo cargar el modelo BERT. Usando TextBlob. Error: {e}")
    from textblob import TextBlob
    sentiment_model = None
    modelo_activo = "textblob"

# ============================================
# 3️⃣ Función principal
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

    # Limpieza básica
    texto = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]", "", observacion).strip()

    # Procesamiento lingüístico (si spaCy está disponible)
    if nlp_spacy:
        doc = nlp_spacy(texto)
        tokens = [t.lemma_.lower() for t in doc if not t.is_stop]
        texto = " ".join(tokens)
    else:
        texto = texto.lower()

    # Evitar errores con texto vacío después de limpieza
    if not texto.strip():
        texto = observacion.strip()

    # ============================================
    # 4️⃣ Análisis de sentimiento
    # ============================================
    if modelo_activo == "bert" and sentiment_model:
        try:
            sentimiento = sentiment_model(texto[:512])[0]
            label = sentimiento["label"].lower()
            if "1" in label or "2" in label:
                tono = "negativo"
            elif "4" in label or "5" in label:
                tono = "positivo"
            else:
                tono = "neutral"
        except Exception as e:
            print(f"⚠️ Error al usar BERT: {e}")
            tono = "neutral"
    else:
        try:
            blob = TextBlob(texto)
            polarity = blob.sentiment.polarity
            if polarity < -0.1:
                tono = "negativo"
            elif polarity > 0.1:
                tono = "positivo"
            else:
                tono = "neutral"
        except Exception as e:
            print(f"⚠️ Error con TextBlob: {e}")
            tono = "neutral"

    # ============================================
    # 5️⃣ Estrategias sugeridas
    # ============================================
    if tono == "negativo":
        estrategia_docente = "Aplicar acompañamiento académico y emocional; reforzar motivación."
        estrategia_psico = "Contactar familia y coordinar apoyo con psicoorientación."
    elif tono == "positivo":
        estrategia_docente = "Reforzar fortalezas y fomentar liderazgo académico."
        estrategia_psico = "Mantener comunicación positiva con la familia."
    else:
        estrategia_docente = "Monitorear progreso; realizar seguimiento quincenal."
        estrategia_psico = "Observar comportamiento y promover espacios de diálogo familiar."

    return tono, estrategia_docente, estrategia_psico
