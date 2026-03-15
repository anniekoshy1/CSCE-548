# init_db.py
import sqlite3
import pathlib
import sys

DB_NAME = "homework.db"   

schema_sql = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL UNIQUE,
    course_name TEXT,
    instructor TEXT
);

CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    course_id INTEGER,
    title TEXT,
    description TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'todo',
    points INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE SET NULL
);
"""

seed_sql = """
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');
INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com');

INSERT INTO courses (course_code, course_name, instructor) VALUES ('CSCE548','Advanced SW','Dr. Smith');
INSERT INTO courses (course_code, course_name, instructor) VALUES ('CSCE101','Intro CS','Prof. Jones');

INSERT INTO assignments (user_id, course_id, title, description, due_date, status, points)
VALUES (1, 1, 'Project 1', 'First project', '2026-04-01', 'todo', 100);

INSERT INTO assignments (user_id, course_id, title, description, due_date, status, points)
VALUES (2, 2, 'Homework 1', 'Chapter 1 problems', '2026-03-30', 'todo', 10);
"""

def main():
    p = pathlib.Path(DB_NAME)
    # If file exists but zero bytes, overwrite it; if it's non-empty, we'll still ensure schema exists
    if p.exists() and p.stat().st_size == 0:
        print(f"{DB_NAME} exists but is empty — will initialize it.")
        p.unlink()  # remove zero-byte file so sqlite creates a fresh one

    conn = sqlite3.connect(DB_NAME)
    try:
        cur = conn.cursor()
        cur.executescript(schema_sql)
        # Insert seed rows only if tables are empty
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.executescript(seed_sql)
            print("Inserted seed data.")
        else:
            print("Tables exist and contain data — no seed inserted.")
        conn.commit()
        print(f"Database initialized: {p.resolve()}")
    except Exception as e:
        print("Error initializing DB:", e)
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()