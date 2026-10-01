
from flask import Flask, request, redirect

app = Flask(__name__)

tasks = [
    {"id": 1, "name": "Create Flask application", "done": True},
    {"id": 2, "name": "Learn Git commands", "done": False},
    {"id": 3, "name": "Deploy app on Render", "done": False}
]

@app.route("/")
def home():
    task_html = ""

    for task in tasks:
        checked = "checked" if task["done"] else ""
        task_html += f"""
        <li>
            <form action="/toggle/{task['id']}" method="POST">
                <button type="submit">
                    {"✅" if task["done"] else "⬜"}
                </button>
                <span style="text-decoration:
                    {"line-through" if task["done"] else "none"}">
                    {task["name"]}
                </span>
            </form>
        </li>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Task Manager</title>
        <style>
            body {{
                font-family: Arial;
                max-width: 600px;
                margin: 60px auto;
                background: #f2f5f9;
            }}
            .container {{
                background: white;
                padding: 25px;
                border-radius: 12px;
            }}
            input, button {{
                padding: 10px;
                margin: 5px;
            }}
            li {{
                list-style: none;
                padding: 10px;
            }}
            form {{
                display: inline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>My Tasks</h1>
            <form action="/add" method="POST">
                <input type="text" name="task"
                       placeholder="Enter a new task" required>
                <button type="submit">Add Task</button>
            </form>
            <ul>{task_html}</ul>
        </div>
    </body>
    </html>
    """

@app.route("/add", methods=["POST"])
def add_task():
    name = request.form.get("task", "").strip()
    if name:
        next_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({
            "id": next_id,
            "name": name,
            "done": False
        })
    return redirect("/")

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)