import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'sql12.freesqldatabase.com'),
        user=os.getenv('DB_USER', 'sql12793988'),
        password=os.getenv('DB_PASSWORD', 'GnXSXZwr5t'),
        database=os.getenv('DB_NAME', 'sql12793988'),  # <-- UPDATED a
        cursorclass=pymysql.cursors.DictCursor

    )   
