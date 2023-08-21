from flask import Flask, render_template
import requests

app = Flask(__name__)

# JSON with posts data
posts = requests.get("https://api.npoint.io/fdafa509912827cfb527").json()


# Home page
@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


# Post page
@app.route("/post/<int:index>")
def post(index):
    target_post = None
    # Check if the ID of the current post matches the requested index
    for post in posts:
        if post["id"] == index:
            target_post = post
    return render_template("post.html", post=target_post)


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
