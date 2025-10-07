import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def train_model():
    df = pd.read_csv("data/students_data.csv")

    features = ["academic_score", "disciplinary_score", "emotional_score"]
    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["profile_cluster"] = model.fit_predict(X_scaled)

    return df, model
