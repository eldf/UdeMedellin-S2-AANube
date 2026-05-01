from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

# Cargar variables de entorno
load_dotenv()


class DataIngestor:
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id

        # --- Lógica de Rutas MLOps ---
        # 1. Obtenemos la ubicación de este script (proyecto/src/ingestion.py)
        script_path = Path(__file__).resolve()

        # 2. Subimos un nivel para llegar a la raíz del proyecto
        self.project_root = script_path.parent.parent

        # 3. Definimos la ruta de datos fuera de /src
        self.raw_path = self.project_root / "data" / "raw"

        # Asegurar que la carpeta existe
        self.raw_path.mkdir(parents=True, exist_ok=True)

        # Inicializar API de Kaggle
        self.api = KaggleApi()
        self.api.authenticate()

    def download_dataset(self):
        """Descarga y extrae el dataset en la carpeta /data de la raíz."""
        print(f"Iniciando descarga en: {self.raw_path}")

        self.api.dataset_download_files(
            self.dataset_id, path=str(self.raw_path), unzip=True
        )
        print("Descarga y extracción completas.")

    def get_dataframe(self, filename: str) -> pd.DataFrame:
        """Carga el archivo desde la ruta de datos externa."""
        file_path = self.raw_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        return pd.read_csv(file_path)


if __name__ == "__main__":
    DATASET_ID = "mlg-ulb/creditcardfraud"

    ingestor = DataIngestor(DATASET_ID)

    try:
        ingestor.download_dataset()
        # Verificar carga
        df = ingestor.get_dataframe("creditcard.csv")
        print(f"Éxito. Datos ubicados en: {ingestor.raw_path}")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
