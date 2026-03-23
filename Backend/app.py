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


if __name__ == '__main__':
    app.run(debug=True)