
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "tasks.db"


# Create database and table
def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# Display all tasks
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


# Add a new task
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()

    if title:
        conn = sqlite3.connect(DATABASE)
        conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


# Mark a task complete or incomplete
@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# Delete a task
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
