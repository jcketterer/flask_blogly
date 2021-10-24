"""Models for Blogly."""
import datetime
from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# Models
DEFAULT_IMG_URL = "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1665&q=80"


class User(db.Model):

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def show_user(self):
        """shows full name of user"""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at}>"

    def readable_date(self):
        """Returns reader friendly date"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", secondary="posts_tags", backref="tags")


class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable=False
    )
