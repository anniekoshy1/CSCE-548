# service.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import business as svc
from db import get_assignment as _get_assignment

app = Flask(__name__)
CORS(app)
# USERS
@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(svc.list_users())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    try:
        uid = svc.add_user(data.get("username"), data.get("email"))
        return jsonify({"user_id": uid}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    u = svc.get_user(user_id)
    if not u:
        return jsonify({"error": "not found"}), 404
    return jsonify(u)

# COURSES
@app.route("/courses", methods=["GET"])
def list_courses():
    return jsonify(svc.list_courses())

@app.route("/courses", methods=["POST"])
def create_course():
    data = request.get_json() or {}
    try:
        cid = svc.add_course(data.get("code"), data.get("name"), data.get("instructor"))
        return jsonify({"course_id": cid}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    c = svc.get_course(course_id)
    if not c:
        return jsonify({"error":"not found"}), 404
    return jsonify(c)

# ASSIGNMENTS
@app.route("/assignments", methods=["GET"])
def all_assignments():
    return jsonify(svc.list_all_assignments())

@app.route("/assignments", methods=["POST"])
def create_assignment():
    data = request.get_json() or {}
    try:
        aid = svc.create_assignment(
            int(data.get("user_id")),
            (int(data.get("course_id")) if data.get("course_id") else None),
            data.get("title"),
            data.get("description"),
            data.get("due_date"),
            data.get("status", "todo"),
            int(data.get("points", 0))
        )
        return jsonify({"assignment_id": aid}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

@app.route("/assignments/<int:aid>", methods=["GET"])
def get_assignment(aid):
    a = _get_assignment(aid)
    if not a:
        return jsonify({"error":"not found"}), 404
    return jsonify(a)

@app.route("/assignments/<int:aid>/done", methods=["POST"])
def mark_done(aid):
    try:
        svc.mark_assignment_done(aid)
        return jsonify({"status":"ok"})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

@app.route("/assignments/<int:aid>", methods=["DELETE"])
def delete_assignment(aid):
    try:
        svc.remove_assignment(aid)
        return jsonify({"status":"deleted"})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)