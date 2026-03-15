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
    return execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )


def get_users():
    return fetch_all(
        "SELECT id, username, email FROM users ORDER BY username"
    )


def get_user(user_id):
    return fetch_one(
        "SELECT id, username, email FROM users WHERE id=?",
        (user_id,)
    )


# NEW: update username/email
def update_user(user_id, username=None, email=None):

    fields = []
    params = []

    if username is not None:
        fields.append("username=?")
        params.append(username)

    if email is not None:
        fields.append("email=?")
        params.append(email)

    if not fields:
        return False

    params.append(user_id)

    query = f"UPDATE users SET {', '.join(fields)} WHERE id=?"

    with closing(get_conn()) as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.rowcount > 0


def update_user_email(user_id, new_email):
    with closing(get_conn()) as conn:
        cur = conn.execute(
            "UPDATE users SET email=? WHERE id=?",
            (new_email, user_id)
        )
        conn.commit()
        return cur.rowcount > 0


def delete_user(user_id):
    with closing(get_conn()) as conn:
        cur = conn.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )
        conn.commit()
        return cur.rowcount > 0


# --- COURSES CRUD ---

def get_courses():
    return fetch_all(
        "SELECT id, course_code, course_name, instructor FROM courses ORDER BY course_code"
    )


def create_course(code, name, instructor=None):
    return execute(
        "INSERT INTO courses (course_code, course_name, instructor) VALUES (?, ?, ?)",
        (code, name, instructor)
    )


def get_course(course_id):
    return fetch_one(
        "SELECT id, course_code, course_name, instructor FROM courses WHERE id=?",
        (course_id,)
    )


# --- ASSIGNMENTS CRUD ---

def create_assignment(user_id, course_id, title, description, due_date, status='todo', points=0):
    return execute(
        """INSERT INTO assignments
        (user_id, course_id, title, description, due_date, status, points)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, course_id, title, description, due_date, status, points)
    )


def get_assignments_for_user(user_id):
    return fetch_all(
        """SELECT a.id, a.user_id, a.course_id, a.title, a.description,
                  a.due_date, a.status, a.points,
                  c.course_code, c.course_name
           FROM assignments a
           LEFT JOIN courses c ON a.course_id = c.id
           WHERE a.user_id = ?
           ORDER BY a.due_date""",
        (user_id,)
    )


def get_all_assignments():
    return fetch_all(
        """SELECT a.id, a.user_id, a.course_id, a.title, a.description,
                  a.due_date, a.status, a.points,
                  u.username AS username,
                  c.course_code AS course_code
           FROM assignments a
           LEFT JOIN users u ON a.user_id = u.id
           LEFT JOIN courses c ON a.course_id = c.id
           ORDER BY a.due_date"""
    )


def get_assignment(assignment_id):
    return fetch_one(
        "SELECT id, user_id, course_id, title, description, due_date, status, points FROM assignments WHERE id=?",
        (assignment_id,)
    )


def update_assignment_status(assignment_id, new_status):
    return execute(
        "UPDATE assignments SET status=? WHERE id=?",
        (new_status, assignment_id)
    )


def update_assignment_points(assignment_id, points):
    return execute(
        "UPDATE assignments SET points=? WHERE id=?",
        (points, assignment_id)
    )


def delete_assignment(assignment_id):
    return execute(
        "DELETE FROM assignments WHERE id=?",
        (assignment_id,)
    )