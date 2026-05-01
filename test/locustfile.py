import random

from locust import HttpUser, between, task


class FraudApiUser(HttpUser):
    # Tiempo de espera entre peticiones (de 0.1 a 0.5 segundos)
    wait_time = between(0.1, 0.5)

    @task
    def predict_fraud(self):
        """
        Simula una petición de predicción con datos aleatorios.
        """
        # Generar datos sintéticos para V1-V28
        payload = {
            "v_features": {f"V{i}": random.uniform(-2, 2) for i in range(1, 29)},
            "amount": random.uniform(10, 5000),
        }

        # Enviar petición POST al endpoint de la API
        self.client.post("/predict", json=payload)

    @task(1)  # Este se ejecuta con menos frecuencia (prioridad)
    def check_health(self):
        self.client.get("/health")
