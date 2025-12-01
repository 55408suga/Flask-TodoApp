from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import *
from schema import *

blp = Blueprint("Tags", "tags", description="Operation on tags", url_prefix="/api")


@blp.route("/tags")
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/tags/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.todos:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            "Could not delete tag. Make sure tag is not associated with any todos, then try again.",
        )


@blp.route("/todos/<int:todo_id>/tag")
class TagsInTodo(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, todo_id):
        todo = TodoModel.query.get_or_404(todo_id)
        return todo.tags


@blp.route("/todos/<int:todo_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(200, TagSchema)
    def post(self, todo_id, tag_id):
        todo = TodoModel.query.get_or_404(todo_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag not in todo.tags:
            todo.tags.append(tag)
            try:
                db.session.add(todo)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occurred while inserting the tag.")
        return tag

    @blp.response(200, TagAndTodoSchema)
    def delete(self, todo_id, tag_id):
        todo = TodoModel.query.get_or_404(todo_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag in todo.tags:
            todo.tags.remove(tag)
            try:
                db.session.add(todo)
                db.session.commit()
            except SQLAlchemyError:
                abort(400, message="An error occurred while deleting the tag.")
        return {"message": "todo removed from tag", "todo": todo, "tag": tag}
