"""
nlp_utils.py
----------------
Módulo de análisis de texto para observaciones docentes.
Genera estrategias pedagógicas, psicoorientación y acciones con la familia
basadas en procesamiento de lenguaje natural (NLP).
"""

from textblob import TextBlob
import re

# ---------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------
def analizar_observacion(texto: str):
    """
    Analiza una observación escrita por el docente y devuelve:
    - tono emocional (positivo / negativo / neutro)
    - estrategia docente sugerida
    - recomendación psicoorientadora o familiar

    Retorna: (tono, estrategia_docente, estrategia_psico_familiar)
    """
    if not texto or not isinstance(texto, str):
        return ("neutro", "Monitoreo general del estudiante.", "Comunicación regular con la familia.")

    texto_limpio = texto.strip().lower()

    # -------------------------------
    # Análisis de sentimiento (TextBlob)
    # -------------------------------
    try:
        blob = TextBlob(texto_limpio)
        sentimiento = blob.sentiment.polarity
        if sentimiento > 0.2:
            tono = "positivo"
        elif sentimiento < -0.2:
            tono = "negativo"
        else:
            tono = "neutro"
    except Exception:
        tono = "neutro"

    # -------------------------------
    # Palabras clave (para contexto)
    # -------------------------------
    academico_bajo = any(p in texto_limpio for p in ["bajo", "deficiente", "dificultad", "mejorar", "fracaso"])
    academico_alto = any(p in texto_limpio for p in ["excelente", "destacado", "sobresaliente", "muy bueno"])
    disciplina_baja = any(p in texto_limpio for p in ["indisciplina", "falta", "conflicto", "castigo", "problema"])
    emocional_inestable = any(p in texto_limpio for p in ["ansioso", "estresado", "triste", "deprimido", "miedo", "aislado"])
    liderazgo = any(p in texto_limpio for p in ["lider", "apoya", "coopera", "ejemplo", "ayuda"])
    familia = any(p in texto_limpio for p in ["padre", "madre", "acudiente", "familia"])

    # -------------------------------
    # Generar estrategias
    # -------------------------------
    estrategia_docente = "Monitoreo y acompañamiento continuo."
    estrategia_psico_familiar = "Comunicación periódica con la familia."

    if academico_bajo:
        estrategia_docente = "Diseñar plan de refuerzo académico personalizado y acompañar el proceso."
        estrategia_psico_familiar = "Involucrar a la familia para reforzar hábitos de estudio en casa."
    elif academico_alto:
        estrategia_docente = "Fomentar retos académicos y liderazgo en el aula."
        estrategia_psico_familiar = "Reconocer logros y fortalecer la motivación intrínseca."
    elif disciplina_baja:
        estrategia_docente = "Aplicar estrategias de disciplina positiva y trabajo colaborativo."
        estrategia_psico_familiar = "Reforzar normas y límites desde el hogar."
    elif emocional_inestable:
        estrategia_docente = "Favorecer ambientes de confianza y apoyo emocional en clase."
        estrategia_psico_familiar = "Remitir a orientación escolar y fomentar comunicación familiar."
    elif liderazgo:
        estrategia_docente = "Potenciar liderazgo y promover tutorías entre pares."
        estrategia_psico_familiar = "Reconocer positivamente el compromiso del estudiante."
    elif familia:
        estrategia_docente = "Coordinar acciones conjuntas con los padres o acudientes."
        estrategia_psico_familiar = "Orientar estrategias familiares para acompañamiento académico."

    # Ajuste según el tono detectado
    if tono == "negativo" and not emocional_inestable:
        estrategia_docente += " Mantener seguimiento cercano para revertir tendencia negativa."
    elif tono == "positivo":
        estrategia_docente += " Reforzar los comportamientos positivos observados."

    return (tono, estrategia_docente, estrategia_psico_familiar)


# ---------------------------------------------------------------------
# Función auxiliar: generar estrategia para una fila (DataFrame)
# ---------------------------------------------------------------------
def generar_estrategias_para_fila(fila):
    """
    Recibe una fila de DataFrame con columna 'Observaciones Docente'
    y devuelve una tupla con (estrategia_docente, estrategia_psico_familiar).
    """
    texto = str(fila.get("Observaciones Docente", ""))
    _, estrategia_docente, estrategia_psico_familiar = analizar_observacion(texto)
    return estrategia_docente, estrategia_psico_familiar


# ---------------------------------------------------------------------
# Función para generar texto completo de informe por grado
# ---------------------------------------------------------------------
def generar_texto_informe_por_grado(df, grado):
    """
    Genera un resumen textual de estrategias docentes para un grado específico.
    """
    df_grado = df[df["Grado"] == grado]
    if df_grado.empty:
        return f"No hay registros disponibles para el grado {grado}."

    resumen = [f"📘 Informe general del grado {grado}\n"]

    for _, fila in df_grado.iterrows():
        nombre = fila.get("Nombre", "Estudiante")
        observacion = fila.get("Observaciones Docente", "")
        tono, estrategia_docente, estrategia_psico_familiar = analizar_observacion(observacion)
        resumen.append(
            f"— **{nombre}** ({tono}):\n"
            f"  - Estrategia docente: {estrategia_docente}\n"
            f"  - Psicoorientación / Familia: {estrategia_psico_familiar}\n"
        )

    return "\n".join(resumen)
