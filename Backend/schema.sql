CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin','teacher','student')) NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT NOT NULL,
    roll_no INTEGER UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);