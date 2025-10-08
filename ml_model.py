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
    columnas = ["]()
