from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

def entrenar_modelo(df):
    """Entrena modelo KMeans y clasifica a los estudiantes"""
    features = df[["Desempeño Académico", "Disciplina", "Aspecto Emocional"]].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    modelo = KMeans(n_clusters=3, random_state=42)
    df["Grupo"] = modelo.fit_predict(X_scaled)
    return df, modelo
