import os
from pathlib import Path
from typing import Dict

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if os.path.exists("/app"):
    mlflow.set_tracking_uri("file:///app/mlruns")
else:
    mlflow.set_tracking_uri(f"file://{Path(__file__).resolve().parent.parent}/mlruns")


# 1. Configuración de Rutas y MLflow


app = FastAPI(
    title="API de Detección de Fraude en Tarjetas de Crédito",
    description="Microservicio para la validación de transacciones en tiempo real.",
    version="1.0.0",
)


# 2. Definición del Esquema de Datos (Validación con Pydantic)
class Transaction(BaseModel):
    # Usamos un diccionario para las 28 variables V para no escribir 28 líneas
    v_features: Dict[str, float] = Field(
        ..., example={f"V{i}": 0.0 for i in range(1, 29)}
    )
    amount: float = Field(..., gt=0, example=150.75)


# Variable global para el modelo (se carga una sola vez al iniciar)
model = None


@app.on_event("startup")
def load_model():
    global model
    try:
        model_name = "DetectorFraudes"
        model_uri = f"models:/{model_name}/latest"
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"✅ Modelo '{model_name}' cargado exitosamente desde el catálogo.")
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")


# 3. Endpoint de Predicción
@app.post("/predict")
async def predict(transaction: Transaction):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible.")

    try:
        # Preparar los datos para el modelo
        data = transaction.v_features.copy()
        data["Amount"] = transaction.amount

        # Convertir a DataFrame (MLflow espera este formato)
        input_df = pd.DataFrame([data])

        # Inferencia
        probability = model.predict_proba(input_df)[:, 1][0]
        prediction = bool(probability > 0.5)

        return {
            "fraud_detected": prediction,
            "fraud_probability": f"{probability * 100:.2f}%",
            "decision": "RECHAZADA" if prediction else "APROBADA",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")


@app.get("/health")
def health_check():
    return {"status": "online", "model_loaded": model is not None}
