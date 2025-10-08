import pandas as pd
from faker import Faker
import random
import os

def generate_fake_students(n=600):
    fake = Faker()
    data = []
    for _ in range(n):
        data.append({
            "ID Estudiante": fake.uuid4(),
            "Nombre": fake.name(),
            "Grado": random.choice(["6A", "6B", "7A", "7B", "8A"]),
            "Desempeño Académico": round(random.uniform(1.0, 5.0), 2),
            "Disciplina": random.randint(0, 10),
            "Aspecto Emocional": random.randint(0, 10),
            "Observaciones Docente": random.choice([
                "Participa activamente",
                "Requiere apoyo emocional",
                "Dificultad con la concentración",
                "Excelente rendimiento",
                "Necesita mejorar la convivencia"
            ])
        })
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/students_data.csv", index=False, encoding="utf-8-sig")
    print("✅ Archivo 'students_data.csv' generado con datos ficticios.")

if __name__ == "__main__":
    generate_fake_students()
