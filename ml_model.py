import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def entrenar_modelo(df):
    """
    Entrena un modelo de agrupamiento K-Means sobre los indicadores
    académicos, de disciplina y emocionales.
    Retorna el dataframe con el grupo asignado y el modelo.
    """

    # Validar columnas necesarias
    columnas = ["Desempeño Académico", "Disciplina", "Aspecto Emocional"]
    for c in columnas:
        if c not in df.columns:
            raise ValueError(f"Falta la columna requerida: {c}")

    # Seleccionar solo las columnas numéricas relevantes
    X = df[columnas].copy()

    # Normalización
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Entrenar modelo de agrupamiento
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    grupos = kmeans.fit_predict(X_scaled)

    # Añadir grupo al dataframe
    df["Grupo"] = grupos

    return df, kmeans
