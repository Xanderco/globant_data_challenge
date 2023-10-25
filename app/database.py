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
    if not data:
        return
    
    columns = ", ".join(data[0].keys())
    placeholders = ", ".join(["%s"] * len(data[0]))
    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    # Convert list of dictionaries to list of tuples
    data_tuples = [tuple(record.values()) for record in data]
    
    connection = create_connection()
    cursor = connection.cursor()
    
    # Execute batch transaction
    cursor.executemany(insert_query, data_tuples)
    
    connection.commit()
    cursor.close()
    connection.close()