from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# DB init for secure comments
def init_db():
    if not os.path.exists("secure_comments.db"):
        conn = sqlite3.connect("secure_comments.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, content TEXT)")
        c.executemany("INSERT INTO comments (content) VALUES (?)", [
            ("Welcome to the secure comment wall!",),
            ("This app escapes inputs to prevent XSS.",),
        ])
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def comment():
    conn = sqlite3.connect("secure_comments.db")
    c = conn.cursor()

    if request.method == "POST":
        content = request.form.get("content")
        c.execute("INSERT INTO comments (content) VALUES (?)", (content,))
        conn.commit()

    c.execute("SELECT content FROM comments")
    comments = c.fetchall()
    conn.close()

    return render_template("comments_secure.html", comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5002)
