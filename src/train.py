from pathlib import Path

import mlflow
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import auc, precision_recall_curve
from sklearn.model_selection import train_test_split


def train_model(csv_path: Path, model_type: str = "xgboost", **kwargs):
    with mlflow.start_run(run_name=f"Train_{model_type}", nested=True):
        df = pd.read_csv(csv_path)

        # Preparación de datos
        X = df.drop(["Class", "Time"], axis=1)
        y = df["Class"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Cálculo de balanceo para XGBoost (Ratio de negativos / positivos)
        ratio = float(y_train.value_counts()[0] / y_train.value_counts()[1])

        if model_type == "rf":
            model = RandomForestClassifier(
                n_estimators=100, max_depth=5, random_state=42
            )
            mlflow.log_param("model_family", "RandomForest")

        elif model_type == "xgboost":
            # scale_pos_weight es vital para el desbalance en fraude
            model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                scale_pos_weight=ratio,
                random_state=42,
            )
            mlflow.log_param("model_family", "XGBoost")
            mlflow.log_param("scale_pos_weight", ratio)

        model.fit(X_train, y_train)

        # Evaluación con Area Under Precision-Recall Curve (mejor que F1 para fraude)
        probs = model.predict_proba(X_test)[:, 1]
        precision, recall, _ = precision_recall_curve(y_test, probs)
        pr_auc = auc(recall, precision)

        mlflow.log_metric("pr_auc", pr_auc)
        mlflow.sklearn.log_model(model, f"modelo_{model_type}")

        # --- AQUÍ VA EL REGISTRO EN EL CATÁLOGO CENTRAL ---
        # Esto guarda el modelo y lo registra con el nombre único
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="modelo_fraude",
            registered_model_name="DetectorFraudes",
        )
        # ---------------------------------------------------

        print(f"--- {model_type.upper()} Finalizado. PR-AUC: {pr_auc:.4f} ---")
        return pr_auc
