import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

def entrenar_modelo(df):
    df = df.dropna(subset=["Desempeño Académico", "Disciplina", "Aspecto Emocional"])
    le = LabelEncoder()
    df["Desempeño Académico"] = le.fit_transform(df["Desempeño Académico"])
    df["Disciplina"] = le.fit_transform(df["Disciplina"])
    df["Aspecto Emocional"] = le.fit_transform(df["Aspecto Emocional"])

    X = df[["Disciplina", "Aspecto Emocional"]]
    y = df["Desempeño Académico"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    reporte = classification_report(y_test, y_pred)

    joblib.dump(modelo, "data/student_model.pkl")
    return modelo, reporte
