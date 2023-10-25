import pytest
from app.app import app


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
    with open('../data_challenge_files/hired_employees.csv', 'rb') as data:
        response = client.post('/upload-csv', content_type='multipart/form-data', data={'file': data, 'type': 'hired_employees'})

    assert response.status_code == 200
    assert b"Data inserted successfully" in response.data