"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
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


@app.errorhandler(404)
def four_oh_four_errors(e):
    """present 404 page"""

    return render_template("404.html"), 404


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
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """Post request handling the form submission"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
        tags=tags,
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
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Takes post edit form submission and updates post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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


################### TAGS ########################


@app.route("/tags")
def tags():
    """Display's page with all tag info"""

    tags = Tag.query.all()
    return render_template("/tags/index.html", tags=tags)


@app.route("/tags/new")
def new_tags():
    """Displays form for a new tag."""

    posts = Post.query.all()
    return render_template("/tags/new.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def new_tag():
    """Manages form submission for new tag creation"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added!")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def show_tags(tag_id):
    """Showing a page with info of tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tags/show.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tags(tag_id):
    """Displays a form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("/tags/edit.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Takes form submission for updating a tag that exists"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited!")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Removes deleted Tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted!")

    return redirect("/tags")
