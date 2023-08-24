from flask import Flask, render_template, redirect, url_for, flash, abort
from flask import request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager
from flask_login import current_user, logout_user
from forms import CreatePostForm, NewUserForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from sqlalchemy.exc import IntegrityError
from functools import wraps
from email.message import EmailMessage
import smtplib

# Insert your credentials here
MY_EMAIL = "..."
MY_PASSWORD = "..."
EMAIL_SMTP_ADDRESS = "..."

# Starts Flask, CKEditor, Bootstrap, flask_sqlalchemy and flask_login
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# Login manager from flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Blog Posts Table
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")


# Users Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


# Comments Table
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


# Starts Gravatar
gravatar = Gravatar(
    app,
    size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None
)


# Admin-only decorator for admin-only pages (new/edit/delete post)
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If ID is not 1 (admin), aborts with error 403
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


with app.app_context():
    db.create_all()


# Home page
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template(
        "index.html",
        all_posts=posts,
        logged_in=current_user.is_authenticated
    )


# Register route
@app.route('/register', methods=["GET", "POST"])
def register():
    form = NewUserForm()
    # If the form is submitted and valid
    if form.validate_on_submit():
        # Creates a new user object with the form information
        new_user = User(
            email=form.email.data,
            # Creates a hashed and salted password
            password=generate_password_hash(form.password.data),
            name=form.name.data
        )
        # Tries to add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
        # If the email already exists in the database
        except IntegrityError:
            flash("You have already signed up with "
                  "that email, log in instead!")
            # Redirects to the login page
            return redirect(url_for('login'))
        # If it is successful
        # Logs in the user
        login_user(new_user)
        # Redirects to the home page
        return redirect(url_for("get_all_posts"))
    return render_template(
        "register.html",
        form=form,
        logged_in=current_user.is_authenticated
    )


# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    # If the form is submitted and valid
    if form.validate_on_submit():
        # Extracts information from the form
        email = form.email.data
        password = form.password.data
        # Searches for email in the database
        user = User.query.filter_by(email=email).first()
        # If found
        if user:
            # Checks password authenticity
            if check_password_hash(user.password, password):
                # Logs in the user
                login_user(user)
                # Redirects to the home page
                return redirect(url_for('get_all_posts'))
            else:
                # If the password is incorrect, displays an error message
                flash('Password incorrect, please try again.')
        else:
            # If the email does not exist in the
            # database, displays an error message
            flash('This email does not exist, please try again.')
    return render_template(
        "login.html",
        form=form,
        logged_in=current_user.is_authenticated
    )


# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


# Show Post route
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    # Queries post by ID
    requested_post = BlogPost.query.get(post_id)
    # Gets all comments from that post
    comments = Comment.query.all()
    form = CommentForm()
    # If the form is submitted and valid
    if form.validate_on_submit():
        # Checks if user is logged when submitting a comment
        if not current_user.is_authenticated:
            flash("You need an account to comment.")
            return redirect(url_for("login"))
        # Creates a new comment object with the form information
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post,
        )
        # Adds the new comment to the database
        db.session.add(new_comment)
        db.session.commit()
        # Redirects to the post page
        return redirect(url_for("show_post", post_id=post_id))
    return render_template(
        "post.html",
        post=requested_post,
        form=form,
        all_comments=comments,
        logged_in=current_user.is_authenticated
    )


# About page
@app.route("/about")
def about():
    return render_template(
        "about.html",
        logged_in=current_user.is_authenticated
    )


# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    # If the user is logged in, autofill name and email
    try:
        user = User.query.get(current_user.id)
    except AttributeError:
        user = None
    # If the user clicked the "Submit" button
    if request.method == "POST":
        data = request.form
        client_name = data["name"]
        client_email = data["email"]
        # client_phone = data["phone"]
        # client_msg = data["message"]
        # Structure email
        message = EmailMessage()
        message['From'] = MY_EMAIL
        message['To'] = client_email
        message['Subject'] = f"Hey {client_name}, we received your message!"
        # Customize your message here
        message.set_content((f"Hello, {client_name}!\n\n"
                             "..."))
        # Send email to user via SMTP
        with smtplib.SMTP(EMAIL_SMTP_ADDRESS, port=587) as server:
            server.starttls()
            server.login(user=MY_EMAIL, password=MY_PASSWORD)
            server.send_message(message)
        # Refresh the page, changing the <h1> element
        return render_template(
            "contact.html",
            sent_form=True,
            user=user,
            logged_in=current_user.is_authenticated
        )
    return render_template(
        "contact.html",
        sent_form=False,
        user=user,
        logged_in=current_user.is_authenticated
    )


# Add New Post route
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    # Displays the form to create a new blog post
    form = CreatePostForm()
    # If the form is submitted and valid, adds the new post to the database
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template(
        "make-post.html",
        form=form,
        logged_in=current_user.is_authenticated
    )


# Edit Post route
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    # Displays the form to edit an existing blog post
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    # If the form is submitted and valid, updates the post in the database
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template(
        "make-post.html",
        form=edit_form,
        logged_in=current_user.is_authenticated
    )


# Delete Post route
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    # Deletes a blog post with the provided post_id from the database
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
