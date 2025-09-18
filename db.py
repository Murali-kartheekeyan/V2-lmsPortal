import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'sql12.freesqldatabase.com'),
        user=os.getenv('DB_USER', 'sql12799116'),
        password=os.getenv('DB_PASSWORD', 'spPmpX2NyE'),
        database=os.getenv('DB_NAME', 'sql12799116'),  # <-- UPDATED a
        cursorclass=pymysql.cursors.DictCursor

    )   

