# Globant's Data Engineering Coding Challenge by Alexander Benitez

A simple Flask API to manage employees, integrated with a MariaDB database. This project demonstrates the capabilities of Flask in handling file uploads (CSVs), interacting with a database, and rendering SQL metrics.

## Features:
1. **CSV Upload**: Upload batches of employee data (up to 1000 rows per batch) to the system.
2. **SQL Metrics**:
   - Retrieve the number of employees hired for each job and department in 2021, divided by quarter.
   - List department IDs, names, and the count of employees in each department.

## Requirements:
- Docker


## Setup:

## Docker Deployment:

Running the Flask Application using Docker simplifies the setup process by containerizing the application and its dependencies. Follow the steps below to get the application up and running using Docker:

1. **Navigate** to the project root directory.

2. **Build the Docker Image**:

   ```bash
   docker-compose up --build
   ```

4. **Access the API**:

   Once the containers are up, you can send requests to the api:
   ```
   http://localhost:5000/
   ```

### Environment Variables with Docker:

Set up your environment variables for your database configuration.
   - `DATABASE_HOST`: Your database host.
   - `DATABASE_PORT`: Your database port (typically 3306 for MariaDB).
   - `DATABASE_USER`: Your database user.
   - `DATABASE_PASSWORD`: Your database password.
   - `DATABASE_DB`: The name of your database.

## API Endpoints:

Below are the main API endpoints of the Flask Employee Management system:

1. **Home Endpoint**:
    - **URL**: `/`
    - **Method**: `GET`
    - **Description**: A simple endpoint to verify the application is running. Responds with a greeting.
    
2. **Upload CSV Endpoint**:
    - **URL**: `/upload-csv`
    - **Method**: `POST`
    - **Description**: Used to upload CSV files containing employee, department, or job data.
    - **Parameters**:
      - `file`: The CSV file to be uploaded.
      - `type`: Type of the CSV being uploaded. Values can be: `hired_employees`, `departments`, or `jobs`.
    - **Response**: A success message if the upload and insertion were successful or an error message otherwise.
    
3. **Employees by Job, Department, and Quarter (2021) Endpoint**:
    - **URL**: `/metrics/employees-by-quarter`
    - **Method**: `GET`
    - **Description**: Retrieves the number of employees hired for each job and department in 2021, divided by quarter.
    - **Response**: A JSON array representing the number of hires per department, job, and quarter in 2021.
    
4. **Department and Employee Count Endpoint**:
    - **URL**: `/metrics/departments-employee-count`
    - **Method**: `GET`
    - **Description**: Retrieves a list of department IDs, names, and the number of employees in each department.
    - **Response**: A JSON array containing the department ID, department name, and the number of employees.