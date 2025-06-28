FROM python:3.12-slim-bookworm

WORKDIR /app

# Instalar dependencias
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar MySQL client
RUN apt-get update && apt-get install -y default-mysql-client

# Copiar el resto del código
COPY . .

# Hacer ejecutable los scripts
RUN chmod +x scripts/wait-for-db.sh 

# Exponer puertos
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


