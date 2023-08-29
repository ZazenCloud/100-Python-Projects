from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# TODO: Home page showing all cafes as a list of cards
@app.route("/")
def home():
    return render_template("index.html")

# TODO: Click one card to go to a specific page with all the info of that cafe

# TODO: Route for adding a cafe (any user can add)
# Display it as 50% opacity with a label (waiting mod approval)

# TODO: Route for reporting a cafe closed (any user can report a cafe closed)
# Display with a red bar in the side (waiting mod confirmation)

# TODO: Route for deleting a cafe


if __name__ == '__main__':
    app.run(debug=True)
