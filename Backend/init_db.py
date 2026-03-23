import sqlite3
connection = sqlite3.connect('erp.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

students_data = [
    ('yash123', 'pass123', 'Yash', 2301456,'2301456@soms.edu.in', 'Gojo Satoru','Ai Hoshino','23-08-2007',7207025173,'2025-2029','Hyderabad, Telengana' ),
    ('rahul123', 'pass123', 'Rahul', 2301457, '2301457@soms.edu.in', 'Sun Space', 'Moon Space', '27-06-2006',8787638176,'2025-2029','Kohima, Nagaland'),
    ('himesh123', 'pass123', 'Himesh', 2301458, '2301458@soms.edu.in',  'Ajit Mondal', 'Supriya Mondal','06-01-2007', 9641487310, '2025-2029','Siliguri, West Bengal')
]

for username, password, name, roll_no, email,father_name, mother_name, dob, mobile_no, admission_year, address in students_data:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, 'student')
    )
    
    user_id = cur.lastrowid

    cur.execute(
        "INSERT INTO students (user_id, name, roll_no, email, father_name, mother_name, dob, mobile_no, admission_year, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, name, roll_no, email,father_name, mother_name, dob, mobile_no, admission_year, address)
    )

staff_data = [
    ('admin123', 'admin123', 'admin', 'Admin User', 'ADM001', 'Administration', 'admin@soms.edu.in', '01-01-1985', 9000000001, '2010-11', 'Kolkata, West Bengal'),
    ('faculty123', 'faculty123', 'teacher', 'Dr. Ramesh Kumar', 'FAC001', 'Oral Biology', 'ramesh@soms.edu.in', '15-06-1980', 9000000002, '2015-16', 'Mumbai, Maharashtra'),
]

for username, password, role, name, faculty_id, department, email, dob, mobile_no, joining_year, address in staff_data:
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role))
    
    user_id = cur.lastrowid
    
    cur.execute(
        "INSERT INTO staff (user_id, name, faculty_id, department, email, dob, mobile_no, joining_year, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, name, faculty_id, department, email, dob, mobile_no, joining_year, address)
    )

connection.commit()
connection.close()
print("Database initialized and 'erp.db' created!")