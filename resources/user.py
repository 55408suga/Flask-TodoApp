from flask import make_response
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import UserModel
from schema import UserSchema

blp = Blueprint("users", "users", description="Operation on users",url_prefix="/api")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the user")
        return "",201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            response = make_response()
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response, 204
        abort(401, "Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        response = make_response()
        set_access_cookies(response,new_token)
        return response,204

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        response = make_response()
        unset_jwt_cookies(response)
        return response,204
#後でredisにblocklist
