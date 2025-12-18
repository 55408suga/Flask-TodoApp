from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import TagModel, TodoModel
from schema import TagSchema, PlainTagSchema

blp = Blueprint("Tags", "tags", description="Operation on tags", url_prefix="/api")


@blp.route("/tags")
class Tags(MethodView):
    @jwt_required()
    @blp.response(200, PlainTagSchema(many=True))
    def get(self):
        access_user = int(get_jwt_identity())
        return TagModel.query.filter(TagModel.user_id == access_user).all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(204)
    def post(self, tag_data):
        access_user = int(get_jwt_identity())
        tag = TagModel(**tag_data, user_id=access_user)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occured while inserting the tag")
        return ""


@blp.route("/tags/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        access_user = int(get_jwt_identity())
        tag = TagModel.query.get_or_404(tag_id)
        if access_user != tag.user_id:
            abort(403, message="Invalid credentials")
        return tag

    @jwt_required()
    @blp.response(204)
    def delete(self, tag_id):
        access_user = int(get_jwt_identity())
        tag = TagModel.query.get_or_404(tag_id)
        if access_user != tag.user_id:
            abort(403, message="Invalid credetials")
        if not tag.todos:
            try:
                db.session.delete(tag)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500, message="An error occurred while deteling the tag")
            return ""
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any todos, then try again.",
        )


@blp.route("/todos/<int:todo_id>/tag")
class TagsInTodo(MethodView):
    @jwt_required()
    @blp.response(200, PlainTagSchema(many=True))
    def get(self, todo_id):
        access_user = int(get_jwt_identity())
        todo = TodoModel.query.get_or_404(todo_id)
        if access_user != todo.user_id:
            abort(403, message="Invalid credentials")
        return todo.tags


@blp.route("/todos/<int:todo_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(204)
    def post(self, todo_id, tag_id):
        access_user = int(get_jwt_identity())
        todo = TodoModel.query.get_or_404(todo_id)
        tag = TagModel.query.get_or_404(tag_id)
        if access_user != tag.user_id or access_user != todo.user_id:
            abort(403, message="Invalid credentials")
        if tag not in todo.tags:
            todo.tags.append(tag)
            try:
                db.session.add(todo)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500, message="An error occurred while inserting the tag.")
        return ""

    @jwt_required()
    @blp.response(204)
    def delete(self, todo_id, tag_id):
        access_user = int(get_jwt_identity())
        todo = TodoModel.query.get_or_404(todo_id)
        tag = TagModel.query.get_or_404(tag_id)
        if access_user != tag.user_id or access_user != todo.user_id:
            abort(403, message="Invalid credentials")
        if tag in todo.tags:
            todo.tags.remove(tag)
            try:
                db.session.add(todo)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500, message="An error occurred while deleting the tag.")
        return ""
