# client.py
import requests, json

BASE = "http://127.0.0.1:5000"

def list_all():
    r = requests.get(BASE + "/assignments")
    print("All assignments (count):", len(r.json()))

def add_user(username, email):
    r = requests.post(BASE + "/users", json={"username": username, "email": email})
    print("add_user:", r.status_code, r.json())

def add_course(code, name, instructor=None):
    r = requests.post(BASE + "/courses", json={"code": code, "name": name, "instructor": instructor})
    print("add_course:", r.status_code, r.json())

def add_assignment(user_id, course_id, title):
    payload = {"user_id": user_id, "course_id": course_id, "title": title}
    r = requests.post(BASE + "/assignments", json=payload)
    print("add_assignment:", r.status_code, r.json())
    return r.json().get("assignment_id")

def mark_done(aid):
    r = requests.post(f"{BASE}/assignments/{aid}/done")
    print("mark_done:", r.status_code, r.json())

def delete_assignment(aid):
    r = requests.delete(f"{BASE}/assignments/{aid}")
    print("delete:", r.status_code, r.json())

def demo_flow():
    list_all()
    add_user("cli_test", "cli_test@example.edu")
    add_course("TEST101", "Client Test", "TA Bot")
    aid = add_assignment(1, 1, "Client-created assignment")
    if aid:
        mark_done(aid)
        delete_assignment(aid)
    list_all()

if __name__ == "__main__":
    demo_flow()
