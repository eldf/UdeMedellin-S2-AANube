from pathlib import Path

import kagglehub
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from prefect import get_run_logger, task


@task(retries=3, retry_delay_seconds=60)
def ingest_data():
    logger = get_run_logger()
    logger.info("Descargando dataset desde Kaggle...")
    path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    df = pd.read_csv(f"{path}/creditcard.csv")
    return df


@task(retries=2, retry_delay_seconds=60)
def download_data():
    """Descarga el dataset desde Kaggle usando kagglehub."""
    print("Descargando dataset...")
    path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    # El path suele ser una carpeta, buscamos el .csv
    import os

    for file in os.listdir(path):
        if file.endswith(".csv"):
            return os.path.join(path, file)


@task
def preprocess_and_clean(df: pd.DataFrame):
    logger = get_run_logger()

    # Lógica de negocio: Evitar pagos dobles
    # Se eliminan transacciones idénticas (mismo Tiempo, Monto y V1-V28)
    initial_count = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_count - len(df)
    logger.info(f"Registros duplicados eliminados: {duplicates_removed}")

    return df


@task(name="Análisis Exploratorio Nativo")
def perform_eda(df: pd.DataFrame):
    logger = get_run_logger()
    logger.info("Se va a realizar EDA sobre los datos proporcionados")
    """
    Realiza un EDA visual y estadístico sin dependencias complejas.
    """
    print(f"📊 Generando visualizaciones para {len(df)} registros")

    df.info()

    # Crear carpeta para los artefactos del EDA
    project_root = Path(__file__).parent.parent
    report_path = project_root / "reports" / "figures"
    report_path.mkdir(parents=True, exist_ok=True)

    # 1. Visualización del Desbalance de Clases
    plt.figure(figsize=(8, 6))
    sns.countplot(x="Class", data=df, palette="viridis")
    plt.title("Distribución de Clases (0: Legítimo, 1: Fraude)")
    plt.yscale("log")  # Escala logarítmica para ver la pequeña barra de fraude
    plt.savefig(report_path / "class_distribution.png")
    plt.close()

    # 2. Correlación de variables con la variable objetivo
    # Tomamos las correlaciones de las variables V1-V28 con 'Class'
    plt.figure(figsize=(12, 8))
    correlations = df.corr()["Class"].drop(["Class", "Time"]).sort_values()
    correlations.plot(kind="barh", color="skyblue")
    plt.title("Correlación de Atributos con Fraude (Class)")
    plt.tight_layout()
    plt.savefig(report_path / "correlations.png")
    plt.close()

    # 3. Análisis de montos (Boxplot)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Class", y="Amount", data=df)
    plt.title("Distribución de Montos por Clase")
    plt.ylim(0, 500)  # Limitamos para ver mejor la caja
    plt.savefig(report_path / "amount_boxplot.png")
    plt.close()

    # 4. Resumen estadístico a texto
    stats = df.describe()
    stats.to_csv(project_root / "reports" / "data_summary.csv")

    print(f"✅ EDA completado. Gráficos guardados en: {report_path}")
    return str(report_path)
