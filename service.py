# service.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import business as svc
from db import get_assignment as _get_assignment

app = Flask(__name__)
CORS(app)

# ---------------- USERS ----------------

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return jsonify(svc.list_users())

    data = request.get_json() or {}
    try:
        uid = svc.add_user(data.get("username"), data.get("email"))
        return jsonify({"user_id": uid}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


@app.route("/users/<int:user_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def user_detail(user_id):

    if request.method == "GET":
        u = svc.get_user(user_id)
        if not u:
            return jsonify({"error": "not found"}), 404
        return jsonify(u)

    if request.method in ("PUT", "PATCH"):
        data = request.get_json() or {}
        try:
            updated = svc.update_user(user_id, data)

            if not updated:
                return jsonify({"error": "user not found"}), 404

            return jsonify(svc.get_user(user_id)), 200
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400

    if request.method == "DELETE":
        try:
            svc.delete_user(user_id)
            return jsonify({"status": "deleted"})
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400


# ---------------- COURSES ----------------

@app.route("/courses", methods=["GET", "POST"])
def courses():

    if request.method == "GET":
        return jsonify(svc.list_courses())

    data = request.get_json() or {}

    try:
        cid = svc.add_course(
            data.get("code"),
            data.get("name"),
            data.get("instructor")
        )
        return jsonify({"course_id": cid}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


@app.route("/courses/<int:course_id>", methods=["GET", "PUT", "PATCH"])
def course_detail(course_id):

    if request.method == "GET":
        c = svc.get_course(course_id)
        if not c:
            return jsonify({"error": "not found"}), 404
        return jsonify(c)

    if request.method in ("PUT", "PATCH"):
        data = request.get_json() or {}

        try:
            updated = svc.update_course(course_id, data)

            if not updated:
                return jsonify({"error": "course not found"}), 404

            return jsonify(svc.get_course(course_id))
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400


# ---------------- ASSIGNMENTS ----------------

@app.route("/assignments", methods=["GET", "POST"])
def assignments():

    if request.method == "GET":
        return jsonify(svc.list_all_assignments())

    data = request.get_json() or {}

    try:
        aid = svc.create_assignment(
            int(data.get("user_id")),
            int(data.get("course_id")) if data.get("course_id") else None,
            data.get("title"),
            data.get("description"),
            data.get("due_date"),
            data.get("status", "todo"),
            int(data.get("points", 0))
        )

        return jsonify({"assignment_id": aid}), 201

    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


@app.route("/assignments/<int:aid>", methods=["GET", "PUT", "PATCH", "DELETE"])
def assignment_detail(aid):

    if request.method == "GET":
        a = _get_assignment(aid)

        if not a:
            return jsonify({"error": "not found"}), 404

        return jsonify(a)

    if request.method in ("PUT", "PATCH"):
        data = request.get_json() or {}

        try:
            svc.update_assignment(aid, data)
            return jsonify({"status": "updated"})
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400

    if request.method == "DELETE":
        try:
            svc.remove_assignment(aid)
            return jsonify({"status": "deleted"})
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400


@app.route("/assignments/<int:aid>/done", methods=["POST"])
def mark_done(aid):

    try:
        svc.mark_assignment_done(aid)
        return jsonify({"status": "ok"})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


# ---------------- HEALTH CHECK ----------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)