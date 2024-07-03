import sys
import os
import pytest

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, Globant, It's Alex" in response.data

def test_upload_csv_endpoint(client):
    data_files = [
        ('/mnt/data/departments.csv', 'departments'),
        ('/mnt/data/jobs.csv', 'jobs'),
        ('/mnt/data/hired_employees.csv', 'hired_employees')
    ]
    
    for file_path, file_type in data_files:
        with open(file_path, 'rb') as data:
            response = client.post('/upload-csv', content_type='multipart/form-data', data={'file': data, 'type': file_type})
            assert response.status_code == 200
            assert b"Data inserted successfully" in response.data

def test_employees_by_quarter(client):
    response = client.get('/metrics/employees-by-quarter')
    assert response.status_code == 200
    assert b"department" in response.data

def test_departments_with_employees(client):
    response = client.get('/metrics/departments-with-employees')
    assert response.status_code == 200
    assert b"department_id" in response.data
