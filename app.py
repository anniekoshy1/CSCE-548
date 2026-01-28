# app.py
from db import get_users, get_courses, get_assignments_for_user, get_all_assignments
from db import create_user, create_course, create_assignment, update_assignment_status, delete_assignment
import sys

def print_users():
    users = get_users()
    print("\nUsers:")
    for u in users:
        print(f"{u['user_id']:>2}: {u['username']} <{u['email']}>")

def print_courses():
    courses = get_courses()
    print("\nCourses:")
    for c in courses:
        print(f"{c['course_id']:>2}: {c['course_code']} - {c['course_name']} ({c['instructor']})")

def view_user_assignments():
    print_users()
    uid = input("Enter user_id to view assignments: ").strip()
    if not uid.isdigit(): return
    rows = get_assignments_for_user(int(uid))
    print(f"\nAssignments for user {uid}:")
    for a in rows:
        print(f"{a['assignment_id']:>3} | {a['due_date'] or 'no-date'} | {a['status']:10} | {a.get('course_code') or 'N/A':8} | {a['title']} ({a['points']} pts)")

def view_all_assignments():
    rows = get_all_assignments()
    print("\nAll assignments:")
    for a in rows:
        print(f"{a['assignment_id']:>3} | user:{a.get('username') or 'N/A':6} | {a['due_date'] or 'no-date'} | {a['status']:10} | {a.get('course_code') or 'N/A':8} | {a['title']}")

def add_user():
    u = input("username: ").strip()
    e = input("email: ").strip()
    create_user(u, e)
    print("user added.")

def add_course():
    code = input("course code (e.g. CSCE548): ").strip()
    name = input("course name: ").strip()
    inst = input("instructor (optional): ").strip()
    create_course(code, name, inst or None)
    print("course added.")

def add_assignment():
    print_users()
    uid = input("user_id: ").strip()
    print_courses()
    cid = input("course_id (or enter for none): ").strip()
    title = input("title: ").strip()
    desc = input("description: ").strip()
    due = input("due date (YYYY-MM-DD or blank): ").strip() or None
    pts = input("points (int, default 0): ").strip() or "0"
    create_assignment(int(uid), int(cid) if cid else None, title, desc, due, 'todo', int(pts))
    print("assignment created.")

def mark_done():
    aid = input("assignment_id to mark done: ").strip()
    if not aid.isdigit(): return
    update_assignment_status(int(aid), 'done')
    print("marked done.")

def remove_assignment():
    aid = input("assignment_id to delete: ").strip()
    if not aid.isdigit(): return
    delete_assignment(int(aid))
    print("deleted.")

def menu():
    while True:
        print("""
Homework Tracker - simple CLI
1) List users
2) List courses
3) View a user's assignments
4) View all assignments
5) Add user
6) Add course
7) Add assignment
8) Mark assignment done
9) Delete assignment
0) Exit
""")
        c = input("choice: ").strip()
        if c == '1': print_users()
        elif c == '2': print_courses()
        elif c == '3': view_user_assignments()
        elif c == '4': view_all_assignments()
        elif c == '5': add_user()
        elif c == '6': add_course()
        elif c == '7': add_assignment()
        elif c == '8': mark_done()
        elif c == '9': remove_assignment()
        elif c == '0': sys.exit(0)
        else: print("bad choice")

if __name__ == '__main__':
    menu()
