from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    todos = db.relationship("TodoModel", back_populates="tags", secondary="todo_tags")
    # 以下いらないかも
    user = db.relationship("UserModel", back_populates="tags")
