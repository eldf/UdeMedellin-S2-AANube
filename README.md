# UdeMedellin-S2-AANube
Proyecto de MLOps para detección de fraude en transacciones con tarjeta de crédito.

Autores:
Diego Fernando Nunez Diaz

Jhonatan Gallego Mosquera

Repositorio
https://github.com/eldf/UdeMedellin-S2-AANube


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

## Modelos de entrenamiento

El pipeline entrena y compara dos modelos de clasificación:

### 1. Random Forest Classifier
- **Descripción**: Modelo de ensamble que combina múltiples árboles de decisión para mejorar la precisión y robustez.
- **Configuración**:
  - `n_estimators=100` (100 árboles en el bosque)
  - `max_depth=5` (profundidad máxima de cada árbol)
  - `random_state=42` (reproducibilidad)
- **Ventajas**: Excelente manejo de datos desbalanceados, interpretable y rápido.

### 2. XGBoost Classifier
- **Descripción**: Algoritmo de boosting extremo que entrena árboles de forma secuencial para corregir errores previos.
- **Configuración**:
  - `n_estimators=100` (100 iteraciones de boosting)
  - `max_depth=5` (profundidad máxima de cada árbol)
  - `learning_rate=0.1` (tasa de aprendizaje)
  - `scale_pos_weight=ratio` (ajuste automático del peso para clase minoritaria - casos de fraude)
- **Ventajas**: Manejo automático del desbalance de clases, generalmente mejor rendimiento en problemas de fraude.

### Métrica de evaluación
- **PR-AUC (Area Under Precision-Recall Curve)**: Métrica preferida para datos desbalanceados como el fraude. Es más informativa que ROC-AUC cuando la clase positiva es rara.

### Registro y seguimiento
Ambos modelos se registran automáticamente en:
- **MLflow**: Almacenamiento local en `mlruns/` con métricas, parámetros y artefactos.
- **Modelo registrado**: Se guarda bajo el nombre `DetectorFraudes` para futuras predicciones.

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
uv sync

### Ejecucion del analisis exploratorio de datos

uv run jupyter notebook notebooks/EDA.ipynb
en caso de presentar problemas lanzarlo con el comando
.venv/bin/python -m notebook notebooks/EDA.ipynb


2. Ejecuta el pipeline:

```bash
python main.py
```

3. O usa `docker-compose`:

```bash
docker-compose up --build -d
```

Ejecucion manual con prefect

uv sync
prefect server start
uv run python src/orchestrator.py

docker-compose build fraud-api
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
