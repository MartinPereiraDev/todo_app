import sys
import pymysql
import os

try:
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'db'),
        user=os.getenv('MYSQL_USER', 'martin_admin'),
        password=os.getenv('MYSQL_PASSWORD', 'martin_321'),
        database=os.getenv('MYSQL_DATABASE', 'todo_db')
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f'Error: {str(e)}')
    sys.exit(1)
