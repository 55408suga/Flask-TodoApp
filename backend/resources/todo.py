from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import TodoModel
from schema import TodoSchema, TodoUpdateSchema

blp = Blueprint("todo", __name__, description="operation on todos", url_prefix="/api")


@blp.route("/todos/<int:todo_id>")
class Todo(MethodView):
    @jwt_required()
    @blp.response(200, TodoSchema)
    def get(self, todo_id):
        access_user = int(get_jwt_identity())
        todo = TodoModel.query.get_or_404(todo_id)
        if access_user != todo.user_id:
            abort(403, message="Invalid credentials")
        return todo

    @jwt_required(fresh=True)
    def delete(self, todo_id):
        access_user = int(get_jwt_identity())
        todo = TodoModel.query.get_or_404(todo_id)
        if access_user != todo.user_id:
            abort(403, message="Invalid credentials")
        try:
            db.session.delete(todo)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="an error occured while deleting the todo")
        return "", 204

    @jwt_required()
    @blp.arguments(TodoUpdateSchema)
    def patch(self, todo_data, todo_id):
        access_user = int(get_jwt_identity())
        todo = TodoModel.query.get_or_404(todo_id)
        if access_user != todo.user_id:
            abort(403, message="Invalid credentials")
        todo.name = todo_data.get("name", todo.name)
        todo.deadline = todo_data.get("deadline", todo.deadline)
        todo.is_done = todo_data.get("is_done", todo.is_done)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while updating the todo")
        return "", 204


@blp.route("/todos")
class TodoList(MethodView):
    @jwt_required()
    @blp.response(200, TodoSchema(many=True))
    def get(self):
        access_user = int(get_jwt_identity())
        name = request.args.get("name")
        if name:
            return TodoModel.query.filter(
                TodoModel.user_id == access_user, TodoModel.name.contains(name)
            ).order_by(TodoModel.created_at.desc(), TodoModel.id.desc()).all()
        return TodoModel.query.filter(TodoModel.user_id == access_user).order_by(TodoModel.created_at.desc(), TodoModel.id.desc()).all()

    @jwt_required()
    @blp.arguments(TodoSchema)
    @blp.response(201, TodoSchema)
    def post(self, todo_data):
        access_user = int(get_jwt_identity())
        todo = TodoModel(**todo_data, user_id=access_user)
        try:
            db.session.add(todo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occured while inserting the todo")
        return todo
