from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

# Retrieve posts data from API
response = requests.get("https://api.npoint.io/799ebbb58189a99199b8")
posts = response.json()
post_objects = []

# Create Post objects for each post in the retrieved data
for post in posts:
    post_object = Post(
        post["title"], post["subtitle"], post["id"], post["body"]
        )
    post_objects.append(post_object)


@app.route('/')
def home():
    # List all posts
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def blog_post(index):
    article = None
    # Find the Post object with the specified index
    for obj in post_objects:
        if obj.id == index:
            article = obj
    # Render selected post data
    return render_template("post.html", post=article)


if __name__ == "__main__":
    app.run(debug=True)
