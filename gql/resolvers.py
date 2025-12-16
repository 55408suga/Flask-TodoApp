from ariadne import ObjectType
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import TodoModel


query = ObjectType("Query")


@query.field("hello")
def resolve_hello(_, info):
    return "Hello GraphQL from separated file!"


@query.field("todos")
def resolve_todos(_, info):
    try:
        verify_jwt_in_request()
        current_user_id = int(get_jwt_identity())
        return TodoModel.query.filter_by(user_id=current_user_id).all()
    except Exception:
        return []


@query.field("todo")
def resolve_todo(_, info, id):
    try:
        verify_jwt_in_request()
        current_user_id = int(get_jwt_identity())
        return TodoModel.query.filter_by(id=id, user_id=current_user_id).first()
    except Exception:
        return None


todo = ObjectType("Todo")


def format_datetime(date_obj):
    return date_obj.isoformat() if date_obj else None


@todo.field("created_at")
def resolve_created_at(obj, _):
    return format_datetime(obj.created_at)


@todo.field("updated_at")
def resolve_updated_at(obj, _):
    return format_datetime(obj.updated_at)


@todo.field("deadline")
def resolve_deadline(obj, _):
    return format_datetime(obj.deadline)
