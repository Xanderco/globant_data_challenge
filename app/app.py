from flask import Flask, request, jsonify
import pandas as pd
from mysql.connector import Error
from database import insert_data
from create_tables import check_and_create_tables

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


if __name__ == '__main__':
    check_and_create_tables() # Check if all required tables are present, if not, creates them
    app.run(host="0.0.0.0",debug=True)
