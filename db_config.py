
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'petersql'
}

def create_connection():
    """ create a database connection to the MySQL database specified by db_config """
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
