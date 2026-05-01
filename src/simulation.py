from pathlib import Path

import mlflow
import numpy as np
import pandas as pd

# Configuración de rutas
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Importante: Asegurar que apunte a la carpeta mlruns correcta
mlflow.set_tracking_uri(f"file://{PROJECT_ROOT}/mlruns")


def simulate_prediction(parameters: dict):
    """
    Carga el modelo usando el Model Registry (Catálogo) de forma automática.
    """
    # Nombre que definiste en train.py: "DetectorFraude_Medellin"
    # Cargamos la versión más reciente (latest)
    model_name = "DetectorFraudes"
    model_uri = f"models:/{model_name}/latest"

    try:
        # Cargar el modelo con la flavor de sklearn para acceder a predict_proba
        model = mlflow.sklearn.load_model(model_uri)

        # Convertir diccionario a DataFrame
        input_df = pd.DataFrame([parameters])

        # Predecir
        probability = model.predict_proba(input_df)[:, 1]
        is_fraud = bool(probability[0] > 0.5)

        return {
            "status": "success",
            "is_fraud": is_fraud,
            "probability": round(float(probability[0]) * 100, 2),
            "model_version": "latest",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "tip": "Asegúrate de haber ejecutado train.py al menos una vez para registrar el modelo.",
        }


if __name__ == "__main__":
    # Simulación de datos
    mock_params = {f"V{i}": np.random.uniform(-1, 1) for i in range(1, 29)}
    mock_params["Amount"] = 100.0

    print("\n--- INICIANDO INFERENCIA DESDE EL CATÁLOGO ---")
    result = simulate_prediction(mock_params)

    if result["status"] == "error":
        print(f"❌ Error: {result['message']}")
    else:
        icono = "🚨" if result["is_fraud"] else "✅"
        print(f"Resultado: {icono} {'FRAUDE' if result['is_fraud'] else 'LEGAL'}")
        print(f"Probabilidad: {result['probability']}%")
