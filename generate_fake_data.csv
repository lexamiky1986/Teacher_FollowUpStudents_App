import pandas as pd
from faker import Faker
import random

def generate_fake_students(n=50):
    fake = Faker()
    data = []
    for _ in range(n):
        data.append({
            "student_id": fake.uuid4(),
            "name": fake.name(),
            "grade": random.choice(["6A", "6B", "7A", "7B", "8A"]),
            "academic_score": round(random.uniform(1.0, 5.0), 2),
            "disciplinary_score": random.randint(0, 10),
            "emotional_score": random.randint(0, 10),
            "teacher_observation": random.choice([
                "Participa activamente",
                "Requiere apoyo emocional",
                "Dificultad con la concentración",
                "Excelente rendimiento",
                "Necesita mejorar la convivencia"
            ])
        })
    df = pd.DataFrame(data)
    df.to_csv("data/students_data.csv", index=False)
    print("✅ Archivo 'students_data.csv' generado con datos fake.")

if __name__ == "__main__":
    generate_fake_students(100)
