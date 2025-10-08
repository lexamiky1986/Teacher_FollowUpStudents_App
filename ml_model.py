# ml_model.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

DATA_PATH = "data/students_data.csv"

def entrenar_modelo(path=DATA_PATH):
    """Carga CSV, entrena KMeans y devuelve DataFrame con columna 'Perfil Clúster' y el modelo."""
    df = pd.read_csv(path, encoding="utf-8-sig")

    # Si hay filas vacías, devolver DataFrame vacío manejable
    if df.empty:
        return df, None

    features = ["Desempeño Académico", "Disciplina", "Aspecto Emocional"]
    X = df[features].fillna(df[features].mean())  # rellenar NA con medias si aplicara

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = model.fit_predict(X_scaled)

    df = df.copy()
    df["Perfil Clúster"] = clusters
    return df, model

def generar_estrategias(df):
    """Genera estrategias personalizadas (docente, psico, familia) usando reglas + keywords."""
    if df.empty:
        return pd.DataFrame(columns=["ID Estudiante","Estrategia Docente","Estrategia Psicoorientación","Estrategia Familiar"])

    estrategias = []
    for _, row in df.iterrows():
        acad = float(row.get("Desempeño Académico", 0))
        disc = float(row.get("Disciplina", 0))
        emo = float(row.get("Aspecto Emocional", 0))
        obs = str(row.get("Observaciones Docente", "")).lower()

        # Keywords
        palabras_conflicto = ["agresiv", "conflict", "pelea", "discute", "irrespeto"]
        palabras_emocionales = ["triste", "ansios", "ansiedad", "aislad", "estresad", "miedo", "depres"]
        palabras_academicas = ["dificultad", "no comprende", "no entiende", "bajo rendimiento", "no entrega", "reprob"]

        temas = set()
        text = obs.lower()
        if any(p in text for p in palabras_conflicto):
            temas.add("conflictos interpersonales")
        if any(p in text for p in palabras_emocionales):
            temas.add("situaciones emocionales")
        if any(p in text for p in palabras_academicas):
            temas.add("bajo rendimiento académico")

        # Estrategia docente
        if acad < 3:
            docente = "Implementar tutoría individualizada y plan de refuerzo, seguimiento de tareas y rutinas."
        elif 3 <= acad < 4:
            docente = "Refuerzo por grupos pequeños y tareas prácticas; seguimiento semanal."
        else:
            docente = "Proponer actividades de liderazgo y retos académicos para mantener motivación."

        # Estrategia psicoorientación
        if emo < 5 or "situaciones emocionales" in temas:
            psico = "Atención psicoorientadora individual: trabajo en manejo emocional y autoestima."
        elif "conflictos interpersonales" in temas:
            psico = "Intervención en habilidades sociales y mediación entre pares."
        else:
            psico = "Acompañamiento preventivo y seguimiento periódico del bienestar emocional."

        # Estrategia familiar
        if disc < 5 or "bajo rendimiento académico" in temas:
            familia = "Coordinar reunión con familia para establecer rutinas y acuerdos de seguimiento."
        elif emo < 5:
            familia = "Orientar a la familia sobre escucha activa y apoyo emocional en casa."
        else:
            familia = "Involucrar a la familia en refuerzo positivo y seguimiento del progreso."

        estrategias.append({
            "ID Estudiante": row["ID Estudiante"],
            "Estrategia Docente": docente,
            "Estrategia Psicoorientación": psico,
            "Estrategia Familiar": familia
        })

    return pd.DataFrame(estrategias)
