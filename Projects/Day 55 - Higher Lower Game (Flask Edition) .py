from flask import Flask
import random

# Generate a random number between 0 and 9
random_num = random.randint(0, 9)

app = Flask(__name__)


@app.route("/")
def guess_game():
    # Display the guess game message and an animated GIF
    return ("<h1>Guess a number between 0 and 9</h1>"
            "<img src=https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif>")


@app.route("/<int:user_num>")
def check_number(user_num):
    if user_num == random_num:
        # Display a success message and multiple animated GIFs
        return ("<h1 style='color:green;'>Oh yes!</h1>"
                "<img src=https://i.giphy.com/media/JGKnY4vr9yVxwgsJZ5/giphy.webp>"
                "<img src=https://i.giphy.com/media/JGKnY4vr9yVxwgsJZ5/giphy.webp>"
                "<img src=https://i.giphy.com/media/JGKnY4vr9yVxwgsJZ5/giphy.webp>")
    elif user_num > random_num:
        # Display a message indicating a high guess and an animated GIF
        return ("<h1 style='color:blue;'>Too high!</h1>"                
                "<img src=https://i.giphy.com/media/RLE2Q5ajPa6GgUxe1z/giphy.gif>"
                "<h1 style='color:blue;'>Try again!</h1>")
    else:
        # Display a message indicating a low guess and an animated GIF
        return ("<h1 style='color:red;'>Too low!</h1>"
                "<img src=https://i.giphy.com/media/26gJA9SSe4m54MYec/giphy.webp>"
                "<h1 style='color:red;'>Try again!</h1>")


if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
