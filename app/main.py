from fastapi import FastAPI
from app.api.routers import tasks, users, tasks_list
from app.infrastructure.database import init_db

# Inicializar la aplicación
app = FastAPI()

# Configurar rutas con prefijos estáticos
app.include_router(tasks.router, prefix="/api/v1/tasks")
app.include_router(tasks_list.router, prefix="/api/v1/tasks_list")
app.include_router(users.router, prefix="/api/v1/users")

@app.on_event("startup")
def on_startup():
    # Inicializar la base de datos
    init_db()