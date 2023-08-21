from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests

# Your TMDB API Key here
TMDB_API_KEY = "..."

# Initialize Flask, Flask_Bootstrap and SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'another_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-movies.db"
Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(1000))
    img_url = db.Column(db.String(250), nullable=False)


# Form for editing movie rating and review
class EditRatingForm(FlaskForm):
    rating = DecimalField("Your Rating (e.g. 7.5)",
                          validators=[DataRequired(),
                                      NumberRange(min=0, max=10)])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


# Form for adding a new movie
class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


# Display all movies, in order of rating
@app.route("/")
def home():
    try:
        # Fetch all movies from the database and order them by rating
        all_movies = Movie.query.order_by(Movie.rating).all()
        # Update the ranking based on the sorted order
        for i in range(len(all_movies)):
            all_movies[i].ranking = len(all_movies) - i
        db.session.commit()
        return render_template("index.html", movies=all_movies)
    except OperationalError:
        # If the database doesn't exist, create it
        db.create_all()
        return render_template("index.html")


# Handle selecting a movie from the list
@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        new_movie = form.title.data
        search_params = {
            "query": new_movie,
            "api_key": TMDB_API_KEY,
        }
        movies = requests.get("https://api.themoviedb.org/3/search/movie",
                              params=search_params).json()['results']
        return render_template("select.html", movies=movies, len=len)
    return render_template("add.html", form=form)


# Handle editing the rating and review of a movie
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    movie = Movie.query.get_or_404(id)
    form = EditRatingForm()
    if form.validate_on_submit():
        # Update the rating and review of the movie in the database
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    else:
        form.rating.render_kw = {"placeholder": f"{movie.rating}"}
        form.review.render_kw = {"placeholder": f"{movie.review}"}
        return render_template('edit.html', form=form, movie=movie)


# Handle finding a movie by its ID using TMDB and adding it to the database
@app.route("/find/<int:id>")
def find(id):
    movie_params = {
            "api_key": TMDB_API_KEY,
    }
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}",
                            params=movie_params).json()
    # Create a new movie object with the response data
    movie = Movie(
        title=response['title'],
        year=response["release_date"].split("-")[0],
        img_url=f"https://image.tmdb.org/t/p/w500{response['poster_path']}",
        description=response["overview"]
    )
    # Add the new movie to the database
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for("edit", id=movie.id))


# Handle deleting a movie from the database
@app.route("/delete/<int:id>")
def delete(id):
    movie = Movie.query.get_or_404(id)
    # Delete the movie from the database
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
