from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TodoModel
from schema import TodoSchema, TodoUpdateSchema

blp = Blueprint("todo", __name__, description="operation on todos", url_prefix="/api")


@blp.route("/todos/<int:todo_id>")
class Todo(MethodView):
    @blp.response(200, TodoSchema)
    def get(self, todo_id):
        todo = TodoModel.query.get_or_404(todo_id)
        return todo

    def delete(self, todo_id):
        todo = TodoModel.query.get_or_404(todo_id)
        try:
            db.session.delete(todo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occured while deleting the todo")
        return "", 204

    @blp.arguments(TodoUpdateSchema)
    def patch(self, todo_data, todo_id):
        todo = TodoModel.query.get_or_404(todo_id)
        todo.name = todo_data.get("name", todo.name)
        todo.deadline = todo_data.get("deadline", todo.deadline)
        todo.is_done = todo_data.get("is_done", todo.is_done)
        db.session.commit()
        return "", 204


@blp.route("/todos")
class TodoList(MethodView):
    @blp.response(200, TodoSchema(many=True))
    def get(self):
        return TodoModel.query.all()

    @blp.arguments(TodoSchema)
    def post(self, todo_data):
        todo = TodoModel(**todo_data)
        try:
            db.session.add(todo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occured while inserting the todo")
        return "", 204
