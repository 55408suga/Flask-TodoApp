from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    todos = db.relation(
        "TodoModel", back_populates="user", lazy="dynamic", cascade="all, delete"
    )
    tags = db.relationship(
        "TagModel", back_populates="user", lazy="dynamic", cascade="all,delete"
    )
