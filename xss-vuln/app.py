from flask import Flask, request, render_template
app = Flask(__name__, template_folder="templates", static_folder="static")

comments = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        comment = request.form.get("comment")
        comments.append(comment)  # No sanitization (XSS vuln)
    return render_template("comments.html", comments=comments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
