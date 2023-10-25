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