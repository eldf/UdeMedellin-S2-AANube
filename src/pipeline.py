from pathlib import Path

import mlflow

from ingestion import DataIngestor
from tasks import perform_eda, preprocess_and_clean
from train import train_model

# Supongamos que tienes estos otros módulos (los crearemos luego)
# from preprocessing import DataCleaner
# from train import ModelTrainer


def run_ml_pipeline():
    # Definir rutas basadas en la ubicación del proyecto
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATASET_ID = "mlg-ulb/creditcardfraud"
    RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "creditcard.csv"

    # Configuración de MLflow
    mlflow.set_experiment("fraude_crediticio_pipeline")

    with mlflow.start_run(run_name="Full_Pipeline_Execution"):
        print("\n>>> INICIANDO PIPELINE DE MLOPS <<<\n")

        # ETAPA 1: Ingesta de Datos
        print("--- Etapa 1: Ingesta ---")
        DATASET_ID = "mlg-ulb/creditcardfraud"
        ingestor = DataIngestor(DATASET_ID)
        ingestor.download_dataset()
        df_raw = ingestor.get_dataframe("creditcard.csv")

        mlflow.log_param("dataset_source", DATASET_ID)
        mlflow.log_param("raw_row_count", len(df_raw))

        # ETAPA 2: Preprocesamiento (Simulado por ahora)
        print("--- Etapa 2: Validacion de datos ---")
        clean_data = preprocess_and_clean(df_raw)
        # Aquí llamarías a: cleaner = DataCleaner(df_raw)
        # df_clean = cleaner.process()
        # mlflow.log_event("datos procesados")

        # ETAPA 3: Entrenamiento (Simulado)
        print("--- Etapa 3: Analisis exploratorios de datos ---")
        perform_eda(clean_data)

        # ETAPA 4: Entrenamiento (Simulado)
        print("--- Etapa 4: Entrenamiento ---")
        modelos_a_probar = ["rf", "xgboost"]
        resultados = {}

        for m in modelos_a_probar:
            print(f"\nEntrenando: {m}...")
            score = train_model(RAW_DATA_FILE, m)
            resultados[m] = score

        # Registrar cuál fue el mejor en este run
        mejor_modelo = max(resultados, key=resultados.get)
        mlflow.log_param("mejor_modelo_detectado", mejor_modelo)

        print("Pipeline finalizado con éxito.")


if __name__ == "__main__":
    run_ml_pipeline()
