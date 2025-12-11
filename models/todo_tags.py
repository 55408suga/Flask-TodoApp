from db import db


class TodoTags(db.Model):
    __tablename__ = "todo_tags"

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey("todos.id"), nullable=False)
    