from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
from email.message import EmailMessage
import smtplib

# Insert your credentials here
MY_EMAIL = "..."
MY_PASSWORD = "..."
EMAIL_SMTP_ADDRESS = "..."

# Starting Flask, CKEditor, Bootstrap and SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Blog post Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm for creating and editing posts
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Home page
@app.route('/')
def get_all_posts():
    # Retrieves all blog posts from the database
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


# Display Post route
@app.route("/post/<int:post_id>")
def show_post(post_id):
    # Retrieves a specific blog post with
    # the provided post_id from the database
    post = BlogPost.query.get(post_id)
    return render_template("post.html", post=post)


# Create Post route
@app.route("/new_post", methods=["GET", "POST"])
def create_post():
    # Displays the form to create a new blog post
    form = CreatePostForm()
    # If the form is submitted and valid, adds the new post to the database
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=datetime.now().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# Edit Post route
@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    # Displays the form to edit an existing blog post
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    # If the form is submitted and valid, updates the post in the database
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, editing=True)


# Delete Post route
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    # Deletes a blog post with the provided post_id from the database
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
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
        return render_template("contact.html", sent_form=True)
    return render_template("contact.html", sent_form=False)


if __name__ == "__main__":
    app.run(debug=True)
