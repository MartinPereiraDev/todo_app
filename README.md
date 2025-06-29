# Todo APP with FastAPI

Esta aplicación es una solución completa para la gestión de tareas y listas de tareas, desarrollada como parte de una evaluación técnica. 

La aplicación permite:

- **Gestión de Usuarios**: Sistema de autenticación y autorización basado en JWT, permitiendo el registro y login de usuarios. (aun no implementado)

- **Gestión de Tareas**: CRUD completo (Crear, Leer, Actualizar, Eliminar) de tareas con las siguientes características:
  - Asignación de tareas a usuarios específicos
  - Asociación opcional a listas de tareas
  - Gestión de estados de tarea (start, pending, in_progress, done)
  - Sistema de prioridades (low, medium, high)
  - Rastreo de progreso (0-100)
  - Sistema de tags (personal, work, home)
- **Gestión de Listas de Tareas**: Creación y gestión de listas de tareas para organizar tareas relacionadas.
- **Seguridad**: Implementación completa de autenticación mediante tokens JWT para asegurar el acceso a recursos sensibles.(aun no implementado)

La aplicación está diseñada siguiendo las mejores prácticas de desarrollo, incluyendo:
- Arquitectura limpia y modular
- Documentación de API completa
- Sistema de pruebas automatizado
- Integración continua con Docker
- Gestión de dependencias y configuración


## Ejecución de la Aplicación

1. Asegurarse de tener Docker Desktop instalado y ejecutándose.

   descarga: https://docs.docker.com/desktop/  

   documentacion: https://docs.docker.com/get-started/ 

2. Crear el entorno virtual:
```bash
python -m venv venv
```
activar el entorno virtual:
```bash
.\venv\Scripts\activate
``` 


3. Ajustar variables de entorno en el archivo .env.

   3a. archivo .env.example para guia de las variables de entorno:
   ```bash
   MySQL Database Configuration
   Change these values to match your MySQL server settings
   MYSQL_ROOT_PASSWORD=your_secure_password
   MYSQL_DATABASE=todo_app
   MYSQL_USER=todo_user
   MYSQL_PASSWORD=todo_password
   more...
   ```

   3b. Crear archivo .env con las variable de entorno descriptas en el archivo .env.example
   ```bash
   MYSQL_ROOT_PASSWORD=your_root_password
   MYSQL_DATABASE=your_database_name
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   ```

4. Iniciar los contenedores:

   4a. Construir la imagen Docker

```bash
docker-compose build --no-cache
```

   4b. Iniciar Docker

```bash
docker-compose up -d
```

   4c. Ver logs

```bash
docker logs todo_app
```
La aplicacion se encuentra corriendo en http://localhost:8000


## Documentacion de la API
Documentacion de la API http://localhost:8000/docs

## Documentación

Para más detalles sobre la arquitectura y decisiones técnicas:

- [ARCHITECTURE.md](app/docs/ARCHITECTURE.md) - Estructura y diseño del proyecto
- [DECISION_LOG.md](app/docs/DECISION_LOG.md) - Registro de decisiones técnicas
- [PENDING.md](app/docs/PENDING.md) - Funcionalidades pendientes


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

