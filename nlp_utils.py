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
        "excelente": ["excelente", "destacado", "alto", "sobresaliente", "avanzado"],
        "desinteres": ["desinteres", "poco participativo", "aburrido", "no entrega"],
        "emocional": ["triste", "deprimido", "ansioso", "angustiado", "afectivo"],
        "familia": ["padre", "madre", "hogar", "familiar", "hermano"]
    }

    for categoria, lista_palabras in palabras_clave.items():
        if any(palabra in texto for palabra in lista_palabras):
            temas.add(categoria)

    return list(temas)


# =============================
# 💡 GENERADOR DE ESTRATEGIAS DOCENTES Y PSICOSOCIALES
# =============================

def generar_estrategia_docente(row):
    """
    Genera una estrategia integral a partir de los puntajes y observaciones.
    Combina análisis NLP con los datos académicos, disciplinarios y emocionales.
    """

    texto = str(row.get("Observaciones Docente", "")).lower()
    tono = analizar_sentimiento(texto)
    temas = detectar_temas(texto)

    estrategias = []

    # --- Estrategias según rendimiento ---
    if row["Desempeño Académico"] < 3:
        estrategias.append("Refuerzo académico individual y revisión de hábitos de estudio.")
    elif row["Desempeño Académico"] >= 4.5:
        estrategias.append("Asignar retos académicos y liderazgo en proyectos grupales.")

    # --- Estrategias según disciplina ---
    if row["Disciplina"] < 5:
        estrategias.append("Implementar plan de mejora conductual con acompañamiento del docente orientador.")
    elif row["Disciplina"] >= 8:
        estrategias.append("Reconocer y mantener su buen comportamiento mediante refuerzos positivos.")

    # --- Estrategias según aspecto emocional ---
    if row["Aspecto Emocional"] < 6:
        estrategias.append("Requiere intervención psicoorientadora y seguimiento emocional.")
    elif row["Aspecto Emocional"] >= 8:
        estrategias.append("Fortalecer liderazgo emocional y empatía con el grupo.")

    # --- Estrategias específicas según NLP ---
    estrategias_contextuales = {
        "ansiedad": [
            "Derivar a psicoorientación para manejo de ansiedad.",
            "Aplicar ejercicios de respiración y relajación antes de evaluaciones."
        ],
        "liderazgo": [
            "Promover tutorías entre pares y liderazgo en clase.",
            "Fomentar participación en actividades escolares representativas."
        ],
        "conflicto": [
            "Realizar mediación de conflictos y trabajo con convivencia escolar.",
            "Coordinar reunión con padres para promover resolución pacífica de problemas."
        ],
        "bajo_rendimiento": [
            "Revisar plan de estudio y estrategias pedagógicas diferenciadas.",
            "Asignar acompañamiento docente en materias críticas."
        ],
        "excelente": [
            "Fomentar autonomía y retos adicionales.",
            "Motivar participación en concursos académicos."
        ],
        "desinteres": [
            "Aplicar metodologías activas para captar su atención.",
            "Planificar actividades lúdico-pedagógicas con relación a sus intereses."
        ],
        "emocional": [
            "Derivar al área psicoorientadora para evaluación emocional.",
            "Fomentar espacios de escucha y diálogo en clase."
        ],
        "familia": [
            "Coordinar reunión con familia para fortalecer apoyo en el hogar.",
            "Enviar informe de seguimiento y estrategias familiares de apoyo."
        ]
    }

    for tema in temas:
        if tema in estrategias_contextuales:
            estrategias.append(random.choice(estrategias_contextuales[tema]))

    # --- Estrategias generales según tono ---
    if len(estrategias) == 0:
        if tono == "positivo":
            estrategias.append("Mantener estrategias actuales y reforzar su motivación.")
        elif tono == "negativo":
            estrategias.append("Identificar causas de dificultad y aplicar plan de mejora integral.")
        else:
            estrategias.append("Continuar con seguimiento regular y observación constante.")

    # --- Estrategia final combinada ---
    estrategia_final = " ".join(estrategias)

    # --- Área de intervención recomendada ---
    if row["Aspecto Emocional"] < 6 or "emocional" in temas:
        area = "Psicoorientación"
    elif row["Disciplina"] < 5 or "conflicto" in temas:
        area = "Convivencia escolar"
    elif row["Desempeño Académico"] < 3:
        area = "Refuerzo académico"
    else:
        area = "Seguimiento general"

    return estrategia_final, area


# =============================
# 🧾 FUNCIONES DE APOYO A PDF
# =============================

def generar_reporte_pdf_por_grado(df, grado):
    """
    Genera texto base para PDF por grado.
    (El PDF se renderiza desde app.py con reportlab)
    """
    estudiantes = df[df["Grado"] == grado]

    reporte = []
    reporte.append(f"REPORTE DE ESTRATEGIAS DOCENTES - GRADO {grado}\n")
    reporte.append("=" * 80 + "\n\n")

    for _, fila in estudiantes.iterrows():
        estrategia, area = generar_estrategia_docente(fila)
        reporte.append(f"👤 {fila['Nombre']} (ID: {fila['ID Estudiante']})\n")
        reporte.append(f"📚 Académico: {fila['Desempeño Académico']:.2f} | "
                       f"⚖️ Disciplina: {fila['Disciplina']} | "
                       f"💬 Emocional: {fila['Aspecto Emocional']}\n")
        reporte.append(f"🧠 Estrategia: {estrategia}\n")
        reporte.append(f"🏫 Área Recomendada: {area}\n")
        reporte.append("-" * 80 + "\n")

    return "\n".join(reporte)
