# db.py
import sqlite3
from contextlib import closing

DB_FILE = "homework.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# --- utility helpers ---
def fetch_all(query, params=()):
    with closing(get_conn()) as conn:
        cur = conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

def fetch_one(query, params=()):
    with closing(get_conn()) as conn:
        cur = conn.execute(query, params)
        row = cur.fetchone()
        return dict(row) if row else None

def execute(query, params=()):
    with closing(get_conn()) as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid

# --- USERS CRUD ---
def create_user(username, email):
    return execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))

def get_users():
    return fetch_all("SELECT * FROM users ORDER BY username")

def get_user(user_id):
    return fetch_one("SELECT * FROM users WHERE user_id=?", (user_id,))

def update_user_email(user_id, new_email):
    return execute("UPDATE users SET email=? WHERE user_id=?", (new_email, user_id))

def delete_user(user_id):
    return execute("DELETE FROM users WHERE user_id=?", (user_id,))

# --- COURSES CRUD ---
def get_courses():
    return fetch_all("SELECT * FROM courses ORDER BY course_code")

def create_course(code, name, instructor=None):
    return execute("INSERT INTO courses (course_code, course_name, instructor) VALUES (?, ?, ?)", (code, name, instructor))

# --- ASSIGNMENTS CRUD ---
def create_assignment(user_id, course_id, title, description, due_date, status='todo', points=0):
    return execute("""INSERT INTO assignments
        (user_id, course_id, title, description, due_date, status, points)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (user_id, course_id, title, description, due_date, status, points))

def get_assignments_for_user(user_id):
    return fetch_all("""SELECT a.*, c.course_code, c.course_name
                        FROM assignments a LEFT JOIN courses c ON a.course_id=c.course_id
                        WHERE a.user_id=?
                        ORDER BY a.due_date""", (user_id,))

def get_all_assignments():
    return fetch_all("""SELECT a.*, u.username, c.course_code FROM assignments a
                        LEFT JOIN users u ON a.user_id=u.user_id
                        LEFT JOIN courses c ON a.course_id=c.course_id
                        ORDER BY a.due_date""")

def get_assignment(assignment_id):
    return fetch_one("SELECT * FROM assignments WHERE assignment_id=?", (assignment_id,))

def update_assignment_status(assignment_id, new_status):
    return execute("UPDATE assignments SET status=? WHERE assignment_id=?", (new_status, assignment_id))

def update_assignment_points(assignment_id, points):
    return execute("UPDATE assignments SET points=? WHERE assignment_id=?", (points, assignment_id))

def delete_assignment(assignment_id):
    return execute("DELETE FROM assignments WHERE assignment_id=?", (assignment_id,))
