# business.py
"""
Business layer for Assignment Tracker.
"""

from db import (
    get_users as _get_users,
    get_user as _get_user,
    create_user as _create_user,
    get_courses as _get_courses,
    create_course as _create_course,
    get_all_assignments as _get_all_assignments,
    get_assignments_for_user as _get_assignments_for_user,
    create_assignment as _create_assignment,
    get_assignment as _get_assignment,
    update_assignment_status as _update_assignment_status,
    update_assignment_points as _update_assignment_points,
    delete_assignment as _delete_assignment,
)

# ---------- Users ----------
def list_users():
    return _get_users()

def add_user(username, email):
    if not username or not email:
        raise ValueError("username and email are required")
    if "@" not in email:
        raise ValueError("invalid email address")
    return _create_user(username, email)

def get_user(user_id):
    return _get_user(user_id)

# ---------- Courses ----------
def list_courses():
    return _get_courses()

def add_course(code, name, instructor=None):
    if not code or not name:
        raise ValueError("course code and name required")
    return _create_course(code, name, instructor)

# ---------- Assignments ----------
def list_all_assignments():
    return _get_all_assignments()

def list_assignments_for_user(user_id):
    u = _get_user(user_id)
    if not u:
        raise ValueError(f"user {user_id} not found")
    return _get_assignments_for_user(user_id)

def create_assignment(user_id, course_id, title, description=None, due_date=None, status='todo', points=0):
    if not title:
        raise ValueError("title required")
    if status not in ('todo', 'in_progress', 'done'):
        raise ValueError("invalid status")
    if points is None:
        points = 0
    return _create_assignment(user_id, course_id, title, description, due_date, status, points)

def mark_assignment_done(assignment_id):
    a = _get_assignment(assignment_id)
    if not a:
        raise ValueError("assignment not found")
    return _update_assignment_status(assignment_id, 'done')

def set_assignment_points(assignment_id, points):
    if points is None or int(points) < 0:
        raise ValueError("points must be >= 0")
    return _update_assignment_points(assignment_id, int(points))

def remove_assignment(assignment_id):
    return _delete_assignment(assignment_id)
