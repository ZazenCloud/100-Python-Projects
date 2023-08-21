from flask import Flask, render_template, request
import requests
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Insert your credentials here
MY_EMAIL = "..."
MY_PASSWORD = "..."
EMAIL_SMTP_ADDRESS = "..."

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
@app.route("/contact", methods=["GET", "POST"])
def contact():
    # If the user clicked the "Submit" button
    if request.method == "POST":
        data = request.form
        client_name = data["name"]
        client_email = data["email"]
        client_phone = data["phone"]
        client_msg = data["message"]
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
    app.run()
