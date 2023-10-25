from flask import Flask, request, jsonify
import pandas as pd
from mysql.connector import Error
from database import insert_data

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
    
    # Read CSV using pandas
    df = pd.read_csv(file)
    
    # Convert the DataFrame to a list of dictionaries for insertion
    data = df.to_dict(orient='records')
    
    # Insert data using database.py
    insert_data(file_type,data)


if __name__ == '__main__':
    app.run(debug=True)
