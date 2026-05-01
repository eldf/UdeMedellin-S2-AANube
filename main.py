import sys
from pathlib import Path

# Añadir 'src' al path para evitar errores de importación
sys.path.append(str(Path(__file__).parent / "src"))

from pipeline import run_ml_pipeline


def main():
    """
    Punto de entrada principal para el ciclo de vida del modelo.
    """
    print("=== SISTEMA DE DETECCIÓN DE FRAUDE (MLOps) ===")

    print("1. Ejecutar Pipeline (Entrenamiento)")
    print("2. Ejecutar Simulación (Inferencia)")
    print("3. Ejecutar API")
    choice = input("Seleccione una opción: ")

    if choice == "1":
        run_ml_pipeline()
        print("\n[PROCESO FINALIZADO]")
        print("Puedes revisar los resultados ejecutando: mlflow ui")
    elif choice == "2":
        import numpy as np

        from simulation import simulate_prediction

        # Podrías pedir el monto por consola
        monto = float(input("Ingrese el monto de la transacción a simular: "))
        params = {f"V{i}": np.random.uniform(-1, 1) for i in range(1, 29)}
        params["Amount"] = monto

        res = simulate_prediction(params)
        print(res)

    elif choice == "3":
        import uvicorn

        print("Iniciando API de Producción...")
        uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)

    else:
        print("Opción no válida. Saliendo.")
        sys.exit(0)


if __name__ == "__main__":
    main()
