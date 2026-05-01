# Usamos una imagen base de Python ligera
FROM python:3.11-slim

# Instalamos uv directamente desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos solo los archivos de dependencias primero para aprovechar el cache de capas
COPY pyproject.toml uv.lock ./

# Instalamos las dependencias (sin instalar el proyecto en modo editable)
RUN uv sync --frozen --no-dev

# Copiamos el código fuente y los directorios necesarios
COPY src/ ./src/
COPY main.py .

# Variables de entorno para que Python no genere .pyc y el buffer sea directo
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar la API
# Usamos 'uv run' para asegurar que se use el entorno virtual creado por uv
CMD ["uv", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]