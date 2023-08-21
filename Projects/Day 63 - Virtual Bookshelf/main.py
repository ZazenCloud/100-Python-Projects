from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),  unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# Home page route to display all books
@app.route('/')
def home():
    try:
        all_books = Book.query.all()
    except OperationalError:
        all_books = None
    return render_template("index.html", books=all_books)

# Handle adding a new book to the database
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            db.create_all()
            new_book = Book(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rating'],
            )
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

# Handle editing the rating of a book
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        with app.app_context():
            book_id = request.form["id"]
            book_to_update = Book.query.get(book_id)
            book_to_update.rating = request.form["rating"]
            db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get('id')
    selected_book = Book.query.get(book_id)
    return render_template("edit.html", book=selected_book)

# Handle deleting a book from the database
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    selected_book = Book.query.get(book_id)
    db.session.delete(selected_book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
