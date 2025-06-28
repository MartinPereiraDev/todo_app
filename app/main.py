from fastapi import FastAPI
from app.api.routers.tasks import router as tasks_router
from app.api.routers.users import router as users_router
from app.infrastructure.database import init_db

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks")
app.include_router(users_router, prefix="/users")

@app.on_event("startup")
def on_startup():
    init_db()