from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.sql import func
from app.extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Category {self.title}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="posts")
    title = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref="categories")
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Post {self.title}>"

    @classmethod
    def search(cls, keyword):
        return cls.query.filter(
            func.lower(cls.title).like(func.lower(f"%{keyword}%"))
            | func.lower(cls.description).like(func.lower(f"%{keyword}%"))
        ).all()
