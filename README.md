# UdeMedellin-S2-AANube
Proyecto de MLOps para detección de fraude en transacciones con tarjeta de crédito.

Autores:
Diego Fernando Nunez Diaz
Jhonatan Gallego Mosquera

## Descripción
Este repositorio contiene un pipeline de ML orientado a detección de fraude con:
- ingesta y descarga de datos desde Kaggle
- preprocesamiento y limpieza básica
- análisis exploratorio de datos (EDA)
- entrenamiento y registro de modelos con MLflow
- simulación de inferencia y API con FastAPI

## Estructura del proyecto

├── `.venv/`                 # Entorno virtual del proyecto
├── `data/`
│   ├── `raw/`               # Datos originales descargados
│   └── `processed/`         # Datos procesados o listos para entrenamiento (si aplica)
├── `notebooks/`             # Notebooks de exploración y análisis
├── `reports/`               # Resultados del EDA y artefactos generados
├── `src/`                   # Código fuente principal
│   ├── `api.py`             # API de inferencia con FastAPI
│   ├── `ingestion.py`       # Descarga y carga de datos desde Kaggle
│   ├── `interface.py`       # Interfaz del proyecto (utilidades compartidas)
│   ├── `pipeline.py`        # Orquestación del pipeline completo
│   ├── `simulation.py`      # Simulación de predicción de fraude
│   ├── `tasks.py`           # Tareas de EDA y limpieza de datos con Prefect
│   └── `train.py`           # Entrenamiento de modelos y logging con MLflow
├── `main.py`                # Entrada principal del proyecto
├── `docker-compose.yml`     # Configuración de contenedores Docker
├── `Dockerfile`             # Imagen de aplicación
├── `pyproject.toml`         # Dependencias y configuración de Python
├── `dvc.yaml`               # Pipeline de DVC / definición de etapas (si aplica)
├── `mlflow.db`              # Base de datos local de MLflow
└── `README.md`              # Documentación del proyecto

## Requisitos
- Python 3.10+
- Kaggle API credentials en `.env`

### Variables de entorno
Crea un archivo `.env` con tus credenciales de Kaggle:

```env
KAGGLE_USERNAME=tu_usuario
KAGGLE_KEY=tu_key
```

Además, descarga tu `kaggle.json` desde Kaggle y colócalo en:

```bash
~/.kaggle/kaggle.json
```

## Uso básico
1. Activa el entorno del proyecto:

```bash
source .venv/bin/activate
```

2. Ejecuta el pipeline:

```bash
python main.py
```

3. O usa `docker-compose`:

```bash
docker-compose up --build -d
```
