from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Colummn(db.String(80),nullable=False,unique=True)
    todos = db.relationship("TodoModel",back_populates="tags",scondary="todo_tags")