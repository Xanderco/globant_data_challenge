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