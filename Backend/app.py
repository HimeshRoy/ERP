from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "http://127.0.0.1:5500"}})

def login(username, password):
    connection = sqlite3.connect('erp.db')
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


if __name__ == '__main__':
    app.run(debug=True)