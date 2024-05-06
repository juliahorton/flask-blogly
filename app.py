"""Blogly Flask application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
import datetime

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = 'itsasecret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# db.create_all()

@app.route("/")
def home_page():
        """Redirect to list of users."""
        
        return redirect("/users")
    

@app.route("/users")
def show_users():
        """Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form."""
    
        users = User.query.order_by(User.last_name, User.first_name).all()

        return render_template("users/index.html", users=users)
    

@app.route("/users/new", methods=["GET"])
def show_add_form():
    """Show an add form for users."""

    return render_template("/users/new.html")
    

@app.route("/users/new", methods=["POST"])
def handle_add_form():
    """Process the add form, adding a new user and going back to /users."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user. Have a button to get to their edit page, and to delete the user."""

    user = User.query.get_or_404(user_id)

    return render_template("users/show.html",user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """Show the page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user."""

    user = User.query.get_or_404(user_id)

    return render_template("/users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def handle_edit_form(user_id):
    """Process the edit form, returning the user to the /users page."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")
    

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete the user."""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Add a new post for the user."""

    user = User.query.get_or_404(user_id)

    return render_template("posts/new.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_new_post(user_id):
    """Process the new post form submission and redirect to user details page."""

    user = User.query.get_or_404(user_id)

    title = request.form["post-title"]
    content = request.form["post-content"]
    created_at = datetime.datetime.now()

    post = Post(title=title, content=content, created_at=created_at, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post details."""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("posts/show.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):    
    """Show form to edit post with option to cancel and return to user detail page."""     

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("posts/edit.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Process the post edit form and return user to post information page."""
    
    post = Post.query.get_or_404(post_id)

    post.title = request.form["post-title"]
    post.content = request.form["post-content"]
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect(f"/users/{user.id}")