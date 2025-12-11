from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel, TodoModel
from schema import TagSchema,PlainTagSchema

blp = Blueprint("Tags", "tags", description="Operation on tags", url_prefix="/api")


@blp.route("/tags")
class Tags(MethodView):
    @blp.response(200, PlainTagSchema(many=True))
    def get(self):
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(204)
    def post(self, tag_data):
        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occured while inserting the tag")
        return ""


@blp.route("/tags/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(204)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.todos:
            try:
                db.session.delete(tag)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500,message="an error occurred while deteling the tag")
            return ""
        abort(
            400,
            message = "Could not delete tag. Make sure tag is not associated with any todos, then try again.",
        )


@blp.route("/todos/<int:todo_id>/tag")
class TagsInTodo(MethodView):
    @blp.response(200, PlainTagSchema(many=True))
    def get(self, todo_id):
        todo = TodoModel.query.get_or_404(todo_id)
        return todo.tags


@blp.route("/todos/<int:todo_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(204)
    def post(self, todo_id, tag_id):
        todo = TodoModel.query.get_or_404(todo_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag not in todo.tags:
            todo.tags.append(tag)
            try:
                db.session.add(todo)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500, message="An error occurred while inserting the tag.")
        return ""

    @blp.response(204)
    def delete(self, todo_id, tag_id):
        todo = TodoModel.query.get_or_404(todo_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag in todo.tags:
            todo.tags.remove(tag)
            try:
                db.session.add(todo)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500, message="An error occurred while deleting the tag.")
        return ""
