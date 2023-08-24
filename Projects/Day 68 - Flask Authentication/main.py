from flask import Flask, render_template, request, url_for, redirect, flash
from flask import send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required
from flask_login import current_user, logout_user
from sqlalchemy.exc import IntegrityError

# Starts Flask, flask_sqlalchemy and flask_login
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# Login manager from flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Database table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Home page
@app.route('/')
def home():
    return render_template(
        "index.html",
        logged_in=current_user.is_authenticated
    )


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If the form is submitted and valid
    if request.method == "POST":
        # Extracts information from the form
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        # Creates a hashed and salted password
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        # Creates a new user object
        new_user = User(
            email=email,
            password=hashed_password,
            name=name
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
        # Redirects to the secret page
        return redirect(url_for("secrets"))
    return render_template(
        "register.html",
        logged_in=current_user.is_authenticated
    )


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the form is submitted and valid, logs in the user.
    if request.method == 'POST':
        # Extracts information from the form
        email = request.form.get('email')
        password = request.form.get('password')
        # Searches for email in the database
        user = User.query.filter_by(email=email).first()
        # If found
        if user:
            # Checks password authenticity
            if check_password_hash(user.password, password):
                # Logs in the user
                login_user(user)
                # Redirects to the secret page
                return redirect(url_for('secrets'))
            else:
                # If the password is incorrect, displays an error message
                flash('Password incorrect, please try again.')
        else:
            # If the email does not exist in the
            # database, displays an error message
            flash('This email does not exist, please try again.')
    return render_template(
        "login.html",
        logged_in=current_user.is_authenticated
    )


# Secret page
@app.route('/secrets')
@login_required
def secrets():
    return render_template(
        "secrets.html",
        name=current_user.name,
        logged_in=True)


# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Download route
@app.route('/download')
@login_required
def download():
    return send_from_directory(
        'static/files', 'cheat_sheet.pdf', as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
