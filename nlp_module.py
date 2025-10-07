from textblob import TextBlob

def analizar_observacion(texto):
    sentimiento = TextBlob(texto).sentiment.polarity
    texto_lower = texto.lower()

    if any(p in texto_lower for p in ["ansioso", "triste", "baja autoestima", "miedo", "inseguro"]):
        categoria = "Apoyo emocional"
        estrategia_docente = "Proponer actividades de refuerzo positivo y crear un ambiente seguro."
        psicoorientacion = "Evaluar causas emocionales; sesiones individuales para fortalecer autoestima."
        familia = "Promover espacios de escucha en casa y validar emociones del estudiante."
    elif any(p in texto_lower for p in ["agresivo", "conflicto", "indisciplina", "respeto"]):
        categoria = "Dificultad conductual"
        estrategia_docente = "Reforzar normas de convivencia y usar mediación positiva."
        psicoorientacion = "Sesiones de control de impulsos o trabajo grupal en resolución de conflictos."
        familia = "Establecer límites claros y coherencia entre escuela y hogar."
    elif any(p in texto_lower for p in ["participa", "liderazgo", "colabora", "destacado"]):
        categoria = "Alto desempeño"
        estrategia_docente = "Delegar liderazgo y fomentar tutorías entre pares."
        psicoorientacion = "Estimular proyectos de autonomía personal y social."
        familia = "Reconocer logros y mantener motivación con nuevos retos."
    elif any(p in texto_lower for p in ["dificultad", "no comprende", "bajo rendimiento", "reprobó"]):
        categoria = "Dificultad académica"
        estrategia_docente = "Aplicar refuerzos diferenciados y adaptar estrategias didácticas."
        psicoorientacion = "Evaluar estilo de aprendizaje; apoyo cognitivo si es necesario."
        familia = "Acompañar tareas y reforzar hábitos de estudio en casa."
    else:
        categoria = "Observación general"
        estrategia_docente = "Continuar seguimiento regular y reforzar aspectos positivos."
        psicoorientacion = "Monitoreo sin intervención directa por ahora."
        familia = "Mantener comunicación constante con el docente."

    return {
        "sentimiento": round(sentimiento, 2),
        "categoria": categoria,
        "estrategia_docente": estrategia_docente,
        "psicoorientacion": psicoorientacion,
        "trabajo_familia": familia
    }
