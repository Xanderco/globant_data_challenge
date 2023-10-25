import mysql.connector
from mysql.connector import Error
import os

DATABASE_CONFIG = {
    'host': os.environ.get('DATABASE_HOST', 'db'), 
    'port': int(os.environ.get('DATABASE_PORT', 3306)), 
    'user': os.environ.get('DATABASE_USER', 'root'),
    'password': os.environ.get('DATABASE_PASSWORD', 'Alex@Globant2023*'),
    'database': os.environ.get('DATABASE_DB', 'globant_flask_db')
}

def create_connection():
    """Create and return a new database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
    return connection

def close_connection(connection):
    """Close the database connection."""
    if connection.is_connected():
        connection.close()

def insert_data(table, data):
    """Insert data into the specified table."""
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    connection = create_connection()
    cursor = connection.cursor()
    for record in data:
        cursor.execute(insert_query, list(record.values()))
    
    connection.commit()
    cursor.close()
    connection.close()