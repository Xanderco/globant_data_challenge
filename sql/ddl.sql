CREATE TABLE jobs (
    job_id INT PRIMARY KEY,
    job_name VARCHAR(255) NOT NULL
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL
);

CREATE TABLE hired_employees (
    emp_id INT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    date_hired DATETIME NOT NULL,
    department_id INT,
    job_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);