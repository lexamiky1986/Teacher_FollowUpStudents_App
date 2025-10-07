import pandas as pd
from sklearn.cluster import KMeans

def train_model(csv_path="data/students_data.csv"):
    df = pd.read_csv(csv_path)
    features = df[["academic_score", "disciplinary_score", "emotional_score"]]

    # Entrenamiento simple: agrupar estudiantes por perfil
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["profile_cluster"] = kmeans.fit_predict(features)

    return df, kmeans
