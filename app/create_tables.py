from mysql.connector import Error
from database import create_connection, close_connection

def check_and_create_tables():
    try:

        conn = create_connection()
        cursor = conn.cursor()

        # Check/Create departments table
        cursor.execute("SHOW TABLES LIKE 'departments'")
        result = cursor.fetchone()
        if not result:
            print("Creating 'departments' table...")
            cursor.execute("""
                CREATE TABLE departments (
                    department_id INT PRIMARY KEY,
                    department_name VARCHAR(255) NOT NULL
                );
            """)
            print("'departments' table created successfully.")

        # Check/Create jobs table
        cursor.execute("SHOW TABLES LIKE 'jobs'")
        result = cursor.fetchone()
        if not result:
            print("Creating 'jobs' table...")
            cursor.execute("""
                CREATE TABLE jobs (
                    job_id INT PRIMARY KEY,
                    job_name VARCHAR(255) NOT NULL
                );
            """)
            print("'jobs' table created successfully.")

        # Check/Create hired_employees table
        cursor.execute("SHOW TABLES LIKE 'hired_employees'")
        result = cursor.fetchone()
        if not result:
            print("Creating 'hired_employees' table...")
            cursor.execute("""
                CREATE TABLE hired_employees (
                    emp_id INT PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    date_hired DATETIME NOT NULL,
                    department_id INT,
                    job_id INT,
                    FOREIGN KEY (department_id) REFERENCES departments(department_id),
                    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
                );
            """)
            print("'hired_employees' table created successfully.")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        close_connection(conn)

if __name__ == '__main__':
    check_and_create_tables()
