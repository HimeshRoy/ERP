import sqlite3
connection = sqlite3.connect('erp.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

students_data = [
    ('yash123', 'pass123', 'Yash', 2301456,'2301456@soms.edu.in' ),
    ('rahul123', 'pass123', 'Rahul', 2301457, '2301457@soms.edu.in'),
    ('himesh123', 'pass123', 'Himesh', 2301458, '2301458@soms.edu.in')
]

for username, password, name, roll_no, email in students_data:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, 'student')
    )
    
    user_id = cur.lastrowid

    cur.execute(
        "INSERT INTO students (user_id, name, roll_no, email) VALUES (?, ?, ?, ?)",
        (user_id, name, roll_no, email)
    )

connection.commit()
connection.close()
print("Database initialized and 'erp.db' created!")