import csv
import random
from pathlib import Path

CARRERAS = ["medicina", "ingenieria", "derecho", "psicologia", "contaduria"]


def generar(n=200, semilla=42, salida="data/postulantes.csv"):
    random.seed(semilla)
    filas = []
    for i in range(1, n + 1):
        ingreso = random.randint(50000, 600000)
        promedio = round(random.uniform(4, 10), 1)
        integrantes = random.randint(1, 8)
        distancia = random.randint(0, 120)
        trabaja = random.choice([True, False])
        carrera = random.choice(CARRERAS)
        filas.append({
            "id": i,
            "nombre": f"Postulante {i}",
            "ingreso_familiar": ingreso,
            "promedio": promedio,
            "integrantes_familia": integrantes,
            "distancia_km": distancia,
            "trabaja": str(trabaja).lower(),
            "carrera": carrera,
        })
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    with open(salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)
    return salida


if __name__ == "__main__":
    ruta = generar()
    print(f"Dataset generado en {ruta}")
