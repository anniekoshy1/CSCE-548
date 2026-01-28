-- seed.sql
-- Run: sqlite3 homework.db < seed.sql

PRAGMA foreign_keys = ON;

-- Users (4)
INSERT OR IGNORE INTO users (username, email) VALUES
 ('alex', 'alex@example.edu'),
 ('jamie', 'jamie@example.edu'),
 ('riley', 'riley@example.edu'),
 ('sam', 'sam@example.edu');

-- Courses (5)
INSERT OR IGNORE INTO courses (course_code, course_name, instructor) VALUES
 ('CSCE548', 'Advanced Software Engineering', 'Dr. White'),
 ('MATH241', 'Calculus III', 'Dr. Green'),
 ('ENGL101', 'Intro to Writing', 'Prof. Blue'),
 ('KINE200', 'Fitness and Health', 'Coach Rose'),
 ('HIST210', 'US History', 'Dr. Black');

-- Assignments: create 52 rows across users/courses
INSERT INTO assignments (user_id, course_id, title, description, due_date, status, points) VALUES
-- Alex assignments (15)
(1, 1, 'Project 1 - Schema', 'Create database schema', '2025-02-15', 'done', 100),
(1, 1, 'Project 2 - DAL', 'Write data access layer', '2025-03-10', 'todo', 100),
(1, 2, 'Calc HW1', 'Integration practice', '2025-02-01', 'done', 10),
(1, 2, 'Calc HW2', 'Series problems', '2025-02-08', 'in_progress', 10),
(1, 3, 'Essay Draft', '300-500 words', '2025-02-05', 'todo', 25),
(1, 4, 'Workout Log Week1', '3 sessions', '2025-01-31', 'done', 0),
(1, 4, 'Meal Plan', 'Track calories 5 days', '2025-02-07', 'in_progress', 0),
(1, 5, 'History Quiz Prep', 'Read ch 3-4', '2025-02-03', 'todo', 20),
(1, 1, 'Code Review', 'Peer review PR', '2025-02-20', 'todo', 10),
(1, 1, 'Unit Tests', 'Cover API', '2025-02-28', 'todo', 30),
(1, 3, 'Peer Review', 'Review partner essay', '2025-02-12', 'todo', 5),
(1, 2, 'Calc Midterm Study', 'Practice problems', '2025-03-01', 'todo', 0),
(1, 5, 'Research Notes', 'Source summaries', '2025-02-14', 'in_progress', 15),
(1, 4, 'Fitness Assessment', 'Record baseline', '2025-01-25', 'done', 0),
(1, 3, 'Final Essay Plan', 'Outline', '2025-04-01', 'todo', 0),

-- Jamie assignments (12)
(2, 1, 'Project 1 - Seed DB', 'Insert test rows', '2025-02-16', 'done', 50),
(2, 2, 'Calc HW3', 'Multivariable integrals', '2025-02-11', 'todo', 10),
(2, 2, 'Calc HW4', 'Partial derivatives', '2025-02-18', 'todo', 10),
(2, 3, 'Reading Response', 'Ch 2 summary', '2025-02-04', 'done', 10),
(2, 3, 'Workshop', 'Attend peer workshop', '2025-02-06', 'in_progress', 0),
(2, 4, 'Cardio Session', '30 minutes run', '2025-01-29', 'done', 0),
(2, 5, 'Essay Source List', 'Collect 5 sources', '2025-02-13', 'todo', 10),
(2, 1, 'Refactor DAL', 'Simplify queries', '2025-03-01', 'todo', 20),
(2, 1, 'Write README', 'How to run project', '2025-02-02', 'done', 5),
(2, 3, 'Grammar Quiz', 'Online quiz', '2025-02-10', 'in_progress', 5),
(2, 4, 'Meal Log', 'Track calories 3 days', '2025-01-30', 'done', 0),
(2, 5, 'History Timeline', 'Make timeline', '2025-02-17', 'todo', 15),

-- Riley assignments (13)
(3, 1, 'Initialize Repo', 'Create GitHub repo', '2025-01-20', 'done', 5),
(3, 1, 'Schema Review', 'Confirm constraints', '2025-01-22', 'done', 10),
(3, 2, 'Calc HW5', 'Vector fields', '2025-02-20', 'todo', 10),
(3, 2, 'Study Group', 'Meet to practice', '2025-01-28', 'done', 0),
(3, 3, 'Portfolio', 'Assemble writing samples', '2025-03-10', 'todo', 30),
(3, 4, 'Strength Day', 'Lift session', '2025-01-27', 'done', 0),
(3, 4, 'Nutrition Log', 'Record meals 7 days', '2025-02-14', 'in_progress', 0),
(3, 5, 'Primary Sources', 'Find 3 sources', '2025-02-25', 'todo', 10),
(3, 1, 'Bug Fix', 'Fix null bug', '2025-02-07', 'in_progress', 10),
(3, 1, 'Integration', 'Merge branches', '2025-02-21', 'todo', 10),
(3, 3, 'Peer Feedback', 'Give feedback', '2025-02-19', 'todo', 5),
(3, 2, 'Calc Project', 'Model problem', '2025-03-15', 'todo', 50),
(3, 5, 'Exam Prep', 'Review notes', '2025-02-28', 'todo', 20),

-- Sam assignments (12)
(4, 1, 'Project 1 - Finalize', 'Finish deliverable', '2025-02-18', 'in_progress', 100),
(4, 2, 'Calc Review', 'Old exams', '2025-02-09', 'in_progress', 0),
(4, 3, 'Essay Final', 'Submit final essay', '2025-04-05', 'todo', 40),
(4, 4, 'HIIT Session', 'Interval training', '2025-01-26', 'done', 0),
(4, 4, 'Track Calories', 'One-week log', '2025-02-21', 'todo', 0),
(4, 5, 'Discussion Post', 'Respond to prompt', '2025-02-08', 'done', 5),
(4, 1, 'Documentation', 'Add comments', '2025-02-03', 'done', 5),
(4, 1, 'Deploy Demo', 'Prepare demo', '2025-02-25', 'todo', 10),
(4, 2, 'Calc HW6', 'Line integrals', '2025-03-01', 'todo', 10),
(4, 3, 'Reading Log', 'Book reflections', '2025-03-20', 'todo', 0),
(4, 5, 'Source Review', 'Check sources accuracy', '2025-02-12', 'in_progress', 10),
(4, 3, 'Revise Draft', 'Incorporate feedback', '2025-03-01', 'todo', 15);
