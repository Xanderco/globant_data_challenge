from flask import Flask, request, jsonify
import pandas as pd
from mysql.connector import Error
from database import insert_data, execute_query
from create_tables import check_and_create_tables
from decimal import Decimal

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Globant, It's Alex"

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Assuming the client will send the file and its type (either departments, jobs, employees)
    file = request.files['file']
    file_type = request.form.get('type')
    if not file_type:
        return jsonify({"error": "Type of CSV not provided"}), 400
    
    # Inject column headers based on the type of CSV
    if file_type == 'hired_employees':
        columns = ['emp_id', 'full_name', 'date_hired', 'department_id', 'job_id']
    elif file_type == 'departments':
        columns = ['department_id', 'department_name']
    elif file_type == 'jobs':
        columns = ['job_id', 'job_name']
    else:
        return jsonify({"error": "Invalid type of CSV provided"}), 400
    
    # Read CSV using pandas with the specified column names
    df = pd.read_csv(file, header=None, names=columns)

    num_rows = df.shape[0]

    # Define the batch size
    batch_size = 1000

    num_batches = (num_rows // batch_size) + (1 if num_rows % batch_size else 0)

    # Handle dirty data
    ##df['date_hired'].fillna("1990-01-01T00:00:00Z", inplace=True)
    ##df.fillna("Blank", inplace=True)  # replace "DEFAULT_VALUE" with an actual value

    # If any value Blank, drop for consistency
    df.dropna(inplace=True)
    
    # Check if date_hired column exists and format it in a way MariaDB Understands
    if 'date_hired' in df.columns:
        df['date_hired'] = pd.to_datetime(df['date_hired']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Execute in batchs of 1000 or less
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = start_idx + batch_size
        batch = df.iloc[start_idx:end_idx]
        data = batch.to_dict(orient='records')
        insert_data(file_type, data)

    return jsonify({"message": "Data inserted successfully"}), 200

@app.route('/metrics/employees-by-quarter', methods=['GET'])
def employees_by_quarter():
    query = """
    SELECT 
        d.department_name AS department,
        j.job_name AS job,
        SUM(CASE WHEN QUARTER(e.date_hired) = 1 THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN QUARTER(e.date_hired) = 2 THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN QUARTER(e.date_hired) = 3 THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN QUARTER(e.date_hired) = 4 THEN 1 ELSE 0 END) AS Q4
    FROM 
        departments d 
    JOIN 
        hired_employees e ON d.department_id = e.department_id
    JOIN 
        jobs j ON e.job_id = j.job_id
    WHERE 
        YEAR(e.date_hired) = 2021 
    GROUP BY 
        d.department_name, j.job_name;
    """
    results = execute_query(query)

    for row in results:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = float(value)

    return jsonify(results)

@app.route('/metrics/departments-with-employees', methods=['GET'])
def departments_with_employees():
    query = """
    SELECT 
        d.department_id, 
        d.department_name, 
        COUNT(e.emp_id) as num_employees 
    FROM 
        departments d 
    LEFT JOIN 
        hired_employees e ON d.department_id = e.department_id 
    GROUP BY 
        d.department_id;
    """
    results = execute_query(query)
    return jsonify(results)


if __name__ == '__main__':
    check_and_create_tables() # Check if all required tables are present, if not, creates them
    app.run(host="0.0.0.0",debug=True)
