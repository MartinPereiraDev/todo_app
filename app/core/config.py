class Config:
    DATABASE_URL = "mysql+pymysql://martin_admin:martin_321@db:3306/todo_db"
    SECRET_KEY = "your-secret-key-here"  # Esto debería ser un valor seguro en producción

config = Config()