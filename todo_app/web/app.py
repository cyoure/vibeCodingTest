from flask import Flask, render_template, redirect, url_for, request, flash

from config import DATA_FILE
from todo.storage import Storage
from todo.service import TodoService
from todo.models import STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE


def create_app(data_file: str = DATA_FILE) -> Flask:
    app = Flask(__name__)
    app.secret_key = "minitask-dev-secret"  # 세션 플래시 메시지용, 배포 시 별도 값 필요

    service = TodoService(Storage(data_file))

    @app.route("/")
    def index():
        todos = service.list_all()
        columns = {
            "todo": [t for t in todos if t.status == STATUS_TODO],
            "in_progress": [t for t in todos if t.status == STATUS_IN_PROGRESS],
            "done": [t for t in todos if t.status == STATUS_DONE],
        }
        return render_template("index.html", columns=columns)

    @app.route("/add", methods=["POST"])
    def add():
        try:
            service.add(request.form.get("title", ""))
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("index"))

    @app.route("/move/<int:todo_id>", methods=["POST"])
    def move(todo_id):
        try:
            service.move(todo_id, request.form.get("status", ""))
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("index"))

    @app.route("/edit/<int:todo_id>", methods=["POST"])
    def edit(todo_id):
        try:
            service.update(todo_id, request.form.get("title", ""))
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("index"))

    @app.route("/delete/<int:todo_id>", methods=["POST"])
    def delete(todo_id):
        try:
            service.delete(todo_id)
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
