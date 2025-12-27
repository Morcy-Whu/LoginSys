from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # 真实项目用环境变量
DB_PATH = "users.db"

# ---------- 工具函数 ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- 页面路由 ----------
@app.route("/")
def login():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------- API：注册 ----------
@app.route("/api/register", methods=["POST"])
def register_api():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return {"error": "Missing username or password"}, 400

    password_hash = generate_password_hash(password)

    try:
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        db.commit()
        return {"success": True}
    except sqlite3.IntegrityError:
        return {"error": "Username already exists"}, 409
    finally:
        db.close()


# ---------- API：登录 ----------
@app.route("/api/login", methods=["POST"])
def login_api():
    username = request.form.get("username")
    password = request.form.get("password")

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    db.close()

    if user is None:
        return {"error": "Invalid credentials"}, 401

    if not check_password_hash(user["password_hash"], password):
        return {"error": "Invalid credentials"}, 401

    # 登录成功 → 写 session
    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return {"success": True}

@app.route("/api/delete_account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return {"error": "Unauthorized"}, 401

    user_id = session["user_id"]

    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    db.close()

    # 删除完账号 → 清 session
    session.clear()

    return {"success": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
