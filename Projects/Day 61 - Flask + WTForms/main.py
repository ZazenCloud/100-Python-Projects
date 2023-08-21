from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


app = Flask(__name__)
app.secret_key = "another_secret_key"
Bootstrap(app)


class MyForm(FlaskForm):
    email = StringField('Email', validators=[
        # Email field is required
        DataRequired(),
        # Validate the format of the email
        Email()])
    password = PasswordField('Password', validators=[
        # Password field is required
        DataRequired(),
        # Password must be at least 8 characters long
        Length(min=8)])
    submit = SubmitField('Log In')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = MyForm()
    if form.validate_on_submit():
        # Check if email and password match the admin credentials
        if (form.email.data == "admin@mail.com" and
                form.password.data == "12345678"):
            # If login is successful, render the 'success' template
            return render_template("success.html")
        else:
            # Else, render the 'denied' template
            return render_template("denied.html")
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
