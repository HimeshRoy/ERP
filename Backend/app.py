from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os  

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'erp.db')

def login(username, password):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()

    cur.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    if user is None:
        connection.close()
        return {"success": False, "message": "Username not found"}

    user_id, stored_password, role = user

    if password != stored_password:
        connection.close()
        return {"success": False, "message": "Incorrect password"}

    result = {"success": True, "role": role, "user_id": user_id}

    if role == "student":
        cur.execute("SELECT name, roll_no, email FROM students WHERE user_id = ?", (user_id,))
        student = cur.fetchone()
        if student:
            name, roll_no, email = student
            result["profile"] = {
                "name": name,
                "roll_no": roll_no,
                "email": email,
            }

    elif role in ("admin", "teacher"):
        cur.execute("SELECT name, email, department FROM staff WHERE user_id = ?", (user_id,))
        staff = cur.fetchone()
        if staff:
            name, email, department = staff
            result["profile"] = {
                "name": name,
                "email": email,
                "department": department,
            }

    connection.close()
    return result


@app.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    result = login(username, password)
    return jsonify(result)


@app.route('/student/profile/<int:user_id>', methods=['GET'])
def get_student_profile(user_id):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    cur.execute("SELECT name, roll_no, email, father_name, mother_name, dob, mobile_no, admission_year, address FROM students WHERE user_id = ?", (user_id,))
    student = cur.fetchone()
    
    connection.close()

    if student is None:
        return jsonify({"success": False, "message": "Profile not found"})

    name, roll_no, email, father_name, mother_name, dob, mobile_no, admission_year, address = student

    return jsonify({
        "name": name,
        "roll_no": roll_no,
        "email": email,
        "father_name": father_name,
        "mother_name": mother_name,
        "dob": dob,
        "mobile": mobile_no,
        "year": admission_year,
        "address": address
    })


@app.route('/staff/profile/<int:user_id>', methods=['GET'])
def get_staff_profile(user_id):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    cur.execute("SELECT name, faculty_id, department, email, dob, mobile_no, joining_year, address FROM staff WHERE user_id = ?", (user_id,))
    staff = cur.fetchone()
    
    connection.close()

    if staff is None:
        return jsonify({"success": False, "message": "Profile not found"})

    name, faculty_id, department, email, dob, mobile_no, joining_year, address = staff

    return jsonify({
        "name": name,
        "faculty_id": faculty_id,
        "department": department,
        "email": email,
        "dob": dob,
        "mobile": mobile_no,
        "joining_year": joining_year,
        "address": address
    })


@app.route('/admin/add-student', methods=['POST'])
def add_student():
    data = request.get_json()
    
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (data['username'], data['password'], 'student'))
        
        user_id = cur.lastrowid
        
        cur.execute("""INSERT INTO students 
            (user_id, name, roll_no, email, father_name, mother_name, dob, mobile_no, admission_year, address) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, data['name'], data['roll_no'], data['email'], 
             data['father_name'], data['mother_name'], data['dob'], 
             data['mobile_no'], data['admission_year'], data['address']))
        
        connection.commit()
        connection.close()
        return jsonify({"success": True, "message": "Student added successfully"})
    
    except Exception as e:
        connection.close()
        return jsonify({"success": False, "message": str(e)})


@app.route('/notifications', methods=['GET'])
def get_notifications():
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    cur.execute("SELECT title, message, date FROM notifications ORDER BY id DESC")
    rows = cur.fetchall()
    
    connection.close()
    
    notifications = []
    for row in rows:
        notifications.append({
            "title": row[0],
            "message": row[1],
            "date": row[2]
        })
    
    return jsonify({"notifications": notifications})


@app.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json()
    
    from datetime import datetime
    date = datetime.now().strftime("%d-%m-%Y")
    
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    cur.execute("INSERT INTO notifications (title, message, date) VALUES (?, ?, ?)",
                (data['title'], data['message'], date))
    
    connection.commit()
    connection.close()
    
    return jsonify({"success": True, "message": "Notification added"})


@app.route('/admin/students', methods=['GET'])
def get_all_students():
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    cur.execute("SELECT id, name, roll_no, email FROM students")
    rows = cur.fetchall()
    
    connection.close()
    
    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "roll_no": row[2],
            "email": row[3]
        })
    
    return jsonify({"students": students})


@app.route('/admin/students', methods=['POST'])
def add_student_v2():
    data = request.get_json()
    
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    try:
        username = str(data['roll_no'])
        password = str(data['roll_no'])

        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, 'student'))
        
        user_id = cur.lastrowid
        
        cur.execute("""INSERT INTO students 
            (user_id, name, roll_no, email, father_name, mother_name, dob, mobile_no, admission_year, address) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, data['name'], data['roll_no'], data['email'],
             data['father_name'], data['mother_name'], data['dob'],
             data['mobile'], data['admission_year'], data['address']))
        
        connection.commit()
        connection.close()
        return jsonify({"success": True, "message": "Student added"})
    
    except Exception as e:
        connection.close()
        return jsonify({"success": False, "message": str(e)})


@app.route('/admin/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    try:
        cur.execute("SELECT user_id FROM students WHERE id = ?", (student_id,))
        row = cur.fetchone()
        
        if row is None:
            connection.close()
            return jsonify({"success": False, "message": "Student not found"})
        
        user_id = row[0]
        
        cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        connection.commit()
        connection.close()
        return jsonify({"success": True, "message": "Student deleted"})
    
    except Exception as e:
        connection.close()
        return jsonify({"success": False, "message": str(e)})


@app.route('/admin/faculty', methods=['GET'])
def get_all_faculty():
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    cur.execute("SELECT id, name, faculty_id, email FROM staff")
    rows = cur.fetchall()
    
    connection.close()
    
    faculty = []
    for row in rows:
        faculty.append({
            "id": row[0],
            "name": row[1],
            "faculty_id": row[2],
            "email": row[3]
        })
    
    return jsonify({"faculty": faculty})


@app.route('/admin/faculty', methods=['POST'])
def add_faculty():
    data = request.get_json()
    
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    try:
        username = str(data['faculty_id'])
        password = str(data['faculty_id'])

        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, 'teacher'))
        
        user_id = cur.lastrowid
        
        cur.execute("""INSERT INTO staff 
            (user_id, name, faculty_id, department, email, dob, mobile_no, joining_year, address) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, data['name'], data['faculty_id'], data['department'],
             data['email'], data['dob'], data['mobile'],
             data['joining_year'], data['address']))
        
        connection.commit()
        connection.close()
        return jsonify({"success": True, "message": "Faculty added"})
    
    except Exception as e:
        connection.close()
        return jsonify({"success": False, "message": str(e)})


@app.route('/admin/faculty/<int:staff_id>', methods=['DELETE'])
def delete_faculty(staff_id):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    
    try:
        cur.execute("SELECT user_id FROM staff WHERE id = ?", (staff_id,))
        row = cur.fetchone()
        
        if row is None:
            connection.close()
            return jsonify({"success": False, "message": "Faculty not found"})
        
        user_id = row[0]
        
        cur.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        connection.commit()
        connection.close()
        return jsonify({"success": True, "message": "Faculty deleted"})
    
    except Exception as e:
        connection.close()
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True)