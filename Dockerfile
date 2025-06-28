FROM python:3.12-slim-bookworm  

WORKDIR /app
ENV PATH="/usr/local/bin:${PATH}"

# Instalar pip y dependencias de Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Hacer ejecutable el script de espera
RUN chmod +x scripts/wait-for-db.sh

# Comando por defecto
CMD ["bash", "scripts/wait-for-db.sh", "db:3306", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


