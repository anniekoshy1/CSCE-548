-- schema.sql
-- Run with: sqlite3 homework.db < schema.sql
PRAGMA foreign_keys = ON;

-- users table
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  created_at TEXT DEFAULT (datetime('now'))
);

-- courses table
CREATE TABLE IF NOT EXISTS courses (
  course_id INTEGER PRIMARY KEY AUTOINCREMENT,
  course_code TEXT NOT NULL,
  course_name TEXT NOT NULL,
  instructor TEXT,
  UNIQUE(course_code)
);

-- assignments table (homework/tasks)
CREATE TABLE IF NOT EXISTS assignments (
  assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  course_id INTEGER,
  title TEXT NOT NULL,
  description TEXT,
  due_date TEXT,             -- ISO date string YYYY-MM-DD
  status TEXT NOT NULL CHECK(status IN ('todo','in_progress','done')),
  points INTEGER CHECK(points >= 0),
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);
