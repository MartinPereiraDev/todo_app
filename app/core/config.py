from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Config:
    DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('MYSQL_DATABASE')}"
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

config = Config()