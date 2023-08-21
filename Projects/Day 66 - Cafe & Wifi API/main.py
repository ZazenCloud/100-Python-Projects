from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Converts the Cafe object to a dictionary for JSON serialization
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    # Retrieves a random cafe from the database
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    # Retrieves all cafes from the database
    cafes = db.session.query(Cafe).all()
    return jsonify([cafe.to_dict() for cafe in cafes])


@app.route("/search")
def search_cafe():
    # Searches for cafes based on the provided location
    search_location = request.args.get("location").title()
    results = Cafe.query.filter_by(location=search_location).all()
    if results:
        # Returns a list of cafes found in the location
        return jsonify([result.to_dict() for result in results])
    else:
        # Returns an error message if no cafes are found in the location
        return jsonify(
            error={
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        )


@app.route("/add", methods=["POST"])
def add_cafe():
    # Adds a new cafe to the database
    new_cafe = Cafe(
        name=request.form['name'],
        map_url=request.form['map_url'],
        img_url=request.form['img_url'],
        location=request.form['location'],
        seats=request.form['seats'],
        has_toilet=bool(request.form['has_toilet']),
        has_wifi=bool(request.form['has_wifi']),
        has_sockets=bool(request.form['has_sockets']),
        can_take_calls=bool(request.form['can_take_calls']),
        coffee_price=request.form['coffee_price'],
    )
    db.session.add(new_cafe)
    db.session.commit()
    # Returns a success response after adding the new cafe
    return jsonify(
        response={
            "Success": "Successfully added the new cafe."
        }
    )


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_cafe_price(cafe_id):
    # Updates the price of a cafe with the provided ID
    new_price = request.args.get("new_price")
    cafe_to_update = db.session.query(Cafe).get(cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        # Returns a success response after updating the cafe's price
        return jsonify(
            response={
                "Success": "Successfully updated the price."
            }
        )
    else:
        # Returns an error response if the cafe with the given ID is not found
        return jsonify(
            error={
                "Not Found": f"Sorry, a cafe with ID {cafe_id} was not found."
            }
        ), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    # Deletes a cafe with the provided ID from the database
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe_to_delete = db.session.query(Cafe).get(cafe_id)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            # Returns a success response after deleting the cafe
            return jsonify(
                response={
                    "Success":
                    "Successfully deleted the cafe from the database."
                }
            )
        else:
            # Returns an error response if the cafe
            # with the given ID is not found
            return jsonify(
                error={
                    "Not Found":
                    f"Sorry, a cafe with ID {cafe_id} was not found."
                }
            ), 403
    else:
        # Returns an error response if the API key is incorrect
        return jsonify(
            {
                "error": "Permission denied. "
                "Make sure you have the correct API key"
            }
        ), 403


if __name__ == '__main__':
    app.run(debug=True)
