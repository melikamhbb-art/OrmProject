from flask import Flask, render_template, request, jsonify
from models.user import User

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    qn = request.args.get("q_name", "").strip()
    qe = request.args.get("q_email", "").strip()
    User.create_table()
    users = User.filter()
    highlight_ids = set()
    if qn or qe:
        filtered = []
        for u in users:
            match_name = qn.lower() in (u.name or "").lower()
            match_email = qe.lower() in u.email.lower()
            if match_name or match_email:
                filtered.append(u)
                highlight_ids.add(u.id)
        users = filtered
    return render_template("index.html", users=users, highlight_ids=highlight_ids)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name") or None
    email = request.form.get("email")
    u = User(name=name, email=email)
    u.save()
    return jsonify({
        "id": u.id,
        "name": u.name,
        "email": u.email
    })

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete(user_id):
    u = User.get(id=user_id)
    if u:
        u.delete()
        return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    User.create_table()
    app.run(debug=True)
