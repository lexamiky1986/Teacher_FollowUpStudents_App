import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def entrenar_modelo(df):
    """
    Entrena un modelo de K-Means sobre los indicadores
    académicos, disciplina y emocionales.
    Retorna el dataframe con el grupo asignado y el modelo.
    """
    columnas = ["Desempeño Académico", "Disciplina", "Aspecto Emocional"]
    for c in columnas:
        if c not in df.columns:
            raise ValueError(f"Falta la columna requerida: {c}")

    X = df[columnas].astype(float).copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    grupos = kmeans.fit_predict(X_scaled)

    df = df.copy()
    df["Grupo"] = grupos

    return df, kmeans
