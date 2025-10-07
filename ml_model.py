import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import random

def entrenar_modelo():
    df = pd.read_csv("data/datos_estudiantes.csv")

    X = df[["Desempeño Académico", "Disciplina", "Aspecto Emocional"]]
    X_scaled = StandardScaler().fit_transform(X)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = model.fit_predict(X_scaled)

    df["Perfil Clúster"] = clusters
    return df, model

def generar_estrategias(df):
    estrategias = []

    for _, row in df.iterrows():
        acad = row["Desempeño Académico"]
        disc = row["Disciplina"]
        emo = row["Aspecto Emocional"]
        obs = str(row["Observaciones Docente"]).lower()

        palabras_conflicto = ["problema", "agresivo", "discute", "irrespeto"]
        palabras_emocionales = ["triste", "ansioso", "aislado", "estresado"]
        palabras_academicas = ["dificultad", "tareas", "bajo", "no entrega"]

        temas = []
        if any(p in obs for p in palabras_conflicto):
            temas.append("conflictos interpersonales")
        if any(p in obs for p in palabras_emocionales):
            temas.append("situaciones emocionales")
        if any(p in obs for p in palabras_academicas):
            temas.append("bajo rendimiento académico")

        # Estrategias coherentes
        if acad < 3:
            docente = "Plan de refuerzo académico individual y hábitos de estudio."
        elif 3 <= acad < 4:
            docente = "Fortalecer trabajo colaborativo y seguimiento personalizado."
        else:
            docente = "Fomentar liderazgo académico con proyectos grupales."

        if emo < 5 or "situaciones emocionales" in temas:
            psico = "Atención psicoorientadora enfocada en manejo emocional y autoestima."
        elif "conflictos interpersonales" in temas:
            psico = "Mediación y resolución de conflictos con pares."
        else:
            psico = "Acompañamiento preventivo para bienestar emocional."

        if disc < 5 or "bajo rendimiento acadéico" in temas:
            familia = "Reunión con familia para fortalecer compromisos y rutinas."
        elif emo < 5:
            familia = "Orientación familiar sobre apoyo emocional y comunicación."
        else:
            familia = "Mantener acompañamiento positivo desde el hogar."

        estrategias.append({
            "ID Estudiante": row["ID Estudiante"],
            "Estrategia Docente": docente,
            "Estrategia Psicoorientación": psico,
            "Estrategia Familiar": familia
        })

    return pd.DataFrame(estrategias)
