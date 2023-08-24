import tkinter as tk
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
random_word = None

try:
    with open("french_to_learn.csv", encoding="utf-8") as file:
        data = pandas.read_csv(file)
except FileNotFoundError:
    # If the file is not found, open the default "french_words.csv" file
    with open("french_words.csv", encoding="utf-8") as file:
        data = pandas.read_csv(file)
finally:
    # Convert the data into a list of dictionaries
    to_learn = data.to_dict(orient="records")


def random_french_word():
    """Selects a random French word from the list of words to learn
    and displays it on a flashcard."""
    global random_word, timer
    # Select a random word from the list of words to learn
    random_word = random.choice(to_learn)
    # Cancel any previous timer
    window.after_cancel(timer)
    # Show the front side of the flashcard
    canvas.itemconfig(card, image=front_img)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=random_word["French"], fill="black")
    # Start the timer to automatically turn the flashcard after 3 seconds
    timer = window.after(3000, turn_card)


def turn_card():
    """Turns the flashcard to reveal the back side with the word in English."""
    # Show the back side of the flashcard
    canvas.itemconfig(card, image=back_img)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=random_word["English"], fill="white")


def known_word():
    """Marks the current word as known and proceeds to the next word."""
    # Remove the current word from the list of words to learn
    to_learn.remove(random_word)
    # Convert the updated list back to a DataFrame
    new_df = pandas.DataFrame(to_learn)
    # Save the updated DataFrame to "french_to_learn.csv" file
    new_df.to_csv("french_to_learn.csv", index=False)
    # Select a new random word from the updated list
    random_french_word()


# Window
window = tk.Tk()
window.title("Flashcards!")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
timer = window.after(3000, turn_card)

# Canvas
canvas = tk.Canvas(width=800, height=526)
front_img = tk.PhotoImage(file="flash_front.png")
back_img = tk.PhotoImage(file="flash_back.png")
card = canvas.create_image(400, 263, image=front_img)
language = canvas.create_text(
    400, 150, text="", fill="black", font=LANGUAGE_FONT
)
word = canvas.create_text(400, 263, text="", fill="black", font=WORD_FONT)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_img = tk.PhotoImage(file="flash_wrong.png")
wrong_button = tk.Button(
    image=wrong_img, highlightthickness=0, command=random_french_word
)
wrong_button.grid(column=0, row=1)
right_img = tk.PhotoImage(file="flash_right.png")
right_button = tk.Button(
    image=right_img, highlightthickness=0, command=known_word
)
right_button.grid(column=1, row=1)

random_french_word()

window.mainloop()
