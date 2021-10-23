"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "dad?"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def root_page():
    """shows the list of post from most recent to oldest"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


########################### USERS #############################


@app.route("/users")
def users_page():
    """shows all users and info"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_users():
    """displays form to add new user"""

    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def new_user_form():
    """Post request to handle form submission"""

    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        img_url=request.form["img_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.show_user()} added!")

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """Display page with info on one user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """show form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """form submission for updating user info"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.show_user()} edited!")

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.show_user()} deleted!")

    return redirect("/users")


################################### POSTS ###################################


@app.route("/users/<int:user_id>/posts/new")
def new_form(user_id):
    """Present form for a new post for that user"""

    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """Post request handling the form submission"""

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form["title"], content=request.form["content"], user=user
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added!")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show the specific post selected"""

    post = Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show the specific post selected"""

    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Takes post edit form submission and updates post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited!")

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted successfully!")

    return redirect(f"/users/{post.user_id}")
