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
            name, roll_no, email= student
            result["profile"] = {
                "name": name,
                "roll_no": roll_no,
                "email": email,
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

if __name__ == '__main__':
    app.run(debug=True)