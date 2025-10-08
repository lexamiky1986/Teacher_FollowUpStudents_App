from textblob import TextBlob
import random
import pandas as pd

def analizar_observacion(texto):
    if not isinstance(texto, str) or texto.strip() == "":
        return "Neutro", "Reforzar seguimiento académico general", "Comunicación básica con familia"

    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity

    if polaridad > 0.2:
        tono = "Positivo"
    elif polaridad < -0.2:
        tono = "Negativo"
    else:
        tono = "Neutro"

    texto_lower = texto.lower()
    estrategias_docente = []
    estrategias_psico = []

    if any(pal in texto_lower for pal in ["desmotivado", "triste", "ansioso", "nervioso"]):
        estrategias_docente.append("Apoyar desde tutoría y reforzar autoestima")
        estrategias_psico.append("Reunión con orientador y familia para acompañamiento emocional")

    if any(pal in texto_lower for pal in ["agresivo", "indisciplinado", "conflicto"]):
        estrategias_docente.append("Aplicar pautas de manejo conductual y diálogo empático")
        estrategias_psico.append("Orientar a los padres sobre límites y rutinas de apoyo")

    if any(pal in texto_lower for pal in ["participativo", "motivado", "responsable", "líder"]):
        estrategias_docente.append("Reconocer su liderazgo y promover tutoría entre pares")
        estrategias_psico.append("Mantener comunicación positiva con familia sobre avances")

    if any(pal in texto_lower for pal in ["rendimiento", "bajo", "nota", "dificultad"]):
        estrategias_docente.append("Implementar plan de refuerzo académico personalizado")
        estrategias_psico.append("Contactar familia para establecer hábitos de estudio")

    if not estrategias_docente:
        if tono == "Positivo":
            estrategias_docente.append("Potenciar fortalezas y promover nuevos retos académicos")
            estrategias_psico.append("Retroalimentar positivamente a la familia")
        elif tono == "Negativo":
            estrategias_docente.append("Realizar seguimiento individual y plan de mejora")
            estrategias_psico.append("Citar familia para apoyo emocional y académico")
        else:
            estrategias_docente.append("Observar evolución y mantener comunicación regular")
            estrategias_psico.append("Orientar familia sobre apoyo cotidiano")

    estrategia_doc = random.choice(estrategias_docente)
    estrategia_psico = random.choice(estrategias_psico)

    return tono, estrategia_doc, estrategia_psico

def generar_texto_informe_por_grado(df, grado):
    df_grado = df[df["Grado"] == grado]

    if df_grado.empty:
        return f"No hay información disponible para el grado {grado}."

    promedio_academico = round(df_grado["Desempeño Académico"].mean(), 2)
    promedio_disciplina = round(df_grado["Disciplina"].mean(), 2)
    promedio_emocional = round(df_grado["Aspecto Emocional"].mean(), 2)

    texto = [
        f"Informe general del grado {grado}",
        "",
        f"Promedio académico: {promedio_academico}",
        f"Promedio en disciplina: {promedio_disciplina}",
        f"Promedio emocional: {promedio_emocional}",
        "",
        "Recomendaciones generales:"
    ]

    tonos = []
    estrategias_doc = []
    estrategias_psico = []

    for _, fila in df_grado.iterrows():
        tono, e_doc, e_psico = analizar_observacion(str(fila["Observaciones Docente"]))
        tonos.append(tono)
        estrategias_doc.append(e_doc)
        estrategias_psico.append(e_psico)

    df_grado["Tono"] = tonos
    df_grado["Estrategia Docente"] = estrategias_doc
    df_grado["Estrategia Psico-Familiar"] = estrategias_psico

    estrategia_doc_pred = df_grado["Estrategia Docente"].mode()[0]
    estrategia_psico_pred = df_grado["Estrategia Psico-Familiar"].mode()[0]
    tono_dominante = df_grado["Tono"].mode()[0]

    texto += [
        f"Tono emocional predominante: {tono_dominante}",
        f"Estrategia docente predominante: {estrategia_doc_pred}",
        f"Estrategia psico-familiar sugerida: {estrategia_psico_pred}",
        "",
        "Lista de estudiantes analizados:"
    ]

    for _, fila in df_grado.iterrows():
        texto.append(f"- {fila['Nombre']}: {fila['Tono']} | {fila['Estrategia Docente']}")

    return "\n".join(texto)
