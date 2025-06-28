FROM python:3.12-slim-bookworm

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip install python-dotenv

# Install MySQL client
RUN apt-get update && apt-get install -y default-mysql-client

# Copy the rest of the code
COPY . .

# Make the scripts executable
RUN chmod +x scripts/wait-for-db.sh 

#  Expose ports
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


