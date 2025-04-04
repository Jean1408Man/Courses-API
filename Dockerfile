# Dockerfile

FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar debugpy (por si no está en requirements.txt)
RUN pip install debugpy

# Copiar el resto del código
COPY . .

ENV PYTHONPATH=/app

# Puerto de FastAPI
EXPOSE 8000
# Puerto para el debugger
EXPOSE 5678

# Comando para arrancar con debugger y esperar conexión de VS Code
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
