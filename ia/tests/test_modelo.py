from ia.modelo import calcular_score, priorizar


def test_score_mayor_para_mas_vulnerable():
    pobre = {"ingreso_familiar": 60000, "integrantes_familia": 7, "distancia_km": 100, "promedio": 8}
    rico = {"ingreso_familiar": 590000, "integrantes_familia": 1, "distancia_km": 2, "promedio": 8}
    assert calcular_score(pobre) > calcular_score(rico)


def test_priorizar_ordena_descendente():
    elegibles = [
        {"id": 1, "ingreso_familiar": 500000, "integrantes_familia": 1, "distancia_km": 5, "promedio": 7},
        {"id": 2, "ingreso_familiar": 70000, "integrantes_familia": 6, "distancia_km": 90, "promedio": 7},
    ]
    ordenados = priorizar(elegibles)
    assert ordenados[0]["id"] == 2
    assert "score" in ordenados[0]


def test_entrenar_modelo_reproduce_score():
    from ia.generar_dataset import generar
    import csv
    generar(n=100, salida="data/postulantes.csv")
    with open("data/postulantes.csv", encoding="utf-8") as f:
        filas = []
        for row in csv.DictReader(f):
            filas.append({
                "ingreso_familiar": int(row["ingreso_familiar"]),
                "integrantes_familia": int(row["integrantes_familia"]),
                "distancia_km": int(row["distancia_km"]),
            })
    from ia.modelo import entrenar_modelo
    _, r2 = entrenar_modelo(filas)
    assert r2 > 0.99
