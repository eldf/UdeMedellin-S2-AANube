import os
from pathlib import Path

from prefect import flow, task

from ingestion import DataIngestor
from train import train_model


# Definimos las tareas
@task(retries=2, retry_delay_seconds=60, name="Ingesta de Datos")
def run_ingestion(dataset_id: str):
    ingestor = DataIngestor(dataset_id)
    ingestor.download_dataset()
    return Path("data/raw/creditcard.csv")


@task(name="Entrenamiento de Modelos")
def run_training(csv_path: Path):
    # Probamos ambos modelos para que el catálogo se actualice
    modelos = ["rf", "xgboost"]
    for m in modelos:
        train_model(csv_path, model_type=m)
    return True


@task(name="Limpieza de Docker")
def restart_api():
    # Reiniciar el contenedor para que cargue el nuevo modelo
    os.system("docker-compose restart fraud-api")


# Definimos el flujo principal
@flow(log_prints=True, name="Pipeline de Detección de Fraude")
def fraud_detection_flow():
    print("Iniciando orquestación con Prefect...")

    # 1. Ingesta
    dataset_id = "mlg-ulb/creditcardfraud"
    data_path = run_ingestion(dataset_id)

    # 2. Entrenamiento
    success = run_training(data_path)

    # 3. Despliegue automático
    if success:
        restart_api()
        print("Pipeline finalizado y API reiniciada con el mejor modelo.")


if __name__ == "__main__":
    fraud_detection_flow()
