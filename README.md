# Todo APP with FastAPI

## Ejecución de la Aplicación

1. Asegurarse de tener Docker Desktop instalado y ejecutándose.

   descarga: https://docs.docker.com/desktop/
   documentacion: https://docs.docker.com/get-started/

2. Ajustar variables de entorno en el archivo .env.

   2a. archivo .env.example para guia de las variables de entorno:
   ```bash
   MySQL Database Configuration
   Change these values to match your MySQL server settings
   MYSQL_ROOT_PASSWORD=your_secure_password
   MYSQL_DATABASE=todo_app
   MYSQL_USER=todo_user
   MYSQL_PASSWORD=todo_password
   more...
   ```

   2b. Crear archivo .env con las variable de entorno descriptas en el archivo .env.example
   ```bash
   MYSQL_ROOT_PASSWORD=your_root_password
   MYSQL_DATABASE=your_database_name
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   ```


3. Iniciar los contenedores:
construir la imagen docker
```bash
docker-compose build --no-cache                                                                   ``` 

iniciar docker
```bash
docker-compose up -d
``` 

ver logs 
```bash
docker logs todo_app
```
La aplicacion se encuentra corriendo en http://localhost:8000


## Documentacion de la API
Documentacion de la API http://localhost:8000/docs

## Testing

1. Crear el entorno virtual python:
```bash
python -m venv venv
```
2. Activar el entorno virtual:
```bash
.\venv\Scripts\activate
```
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar los tests:
```bash
pytest --cov=app
pytest tests/unit/test_user_service.py -v
pytest tests/unit/test_task_service.py -v
python -m pytest -v -s tests/integration/test_user.py
python -m pytest -v -s tests/integration/test_task.py
```

