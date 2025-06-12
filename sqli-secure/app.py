from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("admin", "admin123"))
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("user", "user123"))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    # ✅ Using parameterized queries
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    result = cursor.execute(query, (username, password)).fetchone()
    conn.close()

    if result:
        return f"<h1>Welcome, {result[1]}!</h1>"
    else:
        return render_template("login.html", error="Invalid credentials")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
