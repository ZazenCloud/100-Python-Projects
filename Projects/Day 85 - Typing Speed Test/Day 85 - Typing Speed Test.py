# from tkinter import Tk, Label, Entry, Text, END, StringVar, CHAR, WORD
from tkinter import *
import random
import time
import threading
import words

# Flag to indicate if the countdown has started
countdown_started = False

# Choose 300 random words from the list
random_words = random.choices(words.word_list, k=300)

# Divide the 300 random words in 160 lists of 5 words
num_lines = 60
words_per_line = 5
lines_list = [
    random_words[i * words_per_line : (i + 1) * words_per_line]
    for i in range(num_lines)
]


def start_countdown():
    global countdown_started

    # Set the flag to True
    countdown_started = True
    # Get the current time in seconds
    current_time = time.time()
    # Set the countdown duration to 1 minute
    duration = 60
    # Calculate the end time
    end_time = current_time + duration
    # Create a thread to update the label with the remaining time
    threading.Thread(target=update_label, args=(end_time,)).start()


def update_label(end_time):
    # Get the remaining time in seconds
    remaining_time = int(end_time - time.time())
    # Check if the countdown is over
    if remaining_time <= 0:
        # End test
        pass
    else:
        # Set the label text to the remaining time
        time_left_label.config(text=f"Time left: {str(remaining_time)}")
        # schedule the next update after 1 second
        time.sleep(1)
        update_label(end_time)


def find_and_change(word):
    # remove any previous tags
    text_box.tag_remove("green", "1.0", "end")
    # search for the word from the beginning of the text
    index = text_box.search(word, "1.0", "end")
    print(index)
    # if found, apply the tag to the word
    # end_index = f"{index}+{len(word)}c"
    end_index = f"{index}+{len(word)}c"
    text_box.tag_add("green", index, end_index)


word_index = 0
line_index = 0
written_words = []
current_word = lines_list[0][0]
last_word = ""


def space_action():
    global word_index
    global line_index
    global current_word

    new_word = entry_text.get().lower().strip()
    entry_text.delete(0, END)
    written_words.append(new_word)
    word_index += 1
    if word_index > 4:
        line_index += 1
        word_index = 0
        refresh_text_box()
    current_word = lines_list[line_index][word_index]
    if word_index > 0:
        last_word = lines_list[line_index][word_index - 1]
    else:
        last_word = lines_list[line_index - 1][4]
    find_and_change(current_word)
    index = text_box.search(last_word, "1.0", "end")
    end_index = f"{index}+{len(last_word)}c"
    text_box.tag_remove("white", "1.0", "end")
    if new_word == last_word:
        text_box.tag_add("blue", index, end_index)
    else:
        text_box.tag_add("red", index, end_index)
    print(current_word)
    print(written_words)


# TODO: Correct color for backspace letters


def backspace_action():
    global word_index
    global line_index
    global current_word

    word_index -= 1
    if word_index < 0 and line_index > 0:
        line_index -= 1
        word_index = 4
        refresh_text_box()
    current_word = lines_list[line_index][word_index]
    old_word = written_words.pop(word_index + (5 * line_index))
    find_and_change(current_word)
    entry_text.delete(0, END)
    entry_text.insert(0, old_word)


def refresh_text_box():
    text_box.delete(1.0, END)
    text_box.insert(
        INSERT,
        "\n".join([" ".join(item) for item in lines_list[line_index : line_index + 3]]),
    )
    text_box.delete("1.0 + 3 lines", END)


def compare_letters(current_word):
    word_index = text_box.search(current_word, "1.0", "end")
    captured_text = entry_text.get()
    letter_index = int(word_index.split(".")[-1]) + len(captured_text) - 1
    last_letter = captured_text[-1]
    if last_letter == current_word[len(captured_text) - 1]:
        text_box.tag_add("white", f"1.{letter_index}")
    else:
        text_box.tag_add("red", f"1.{letter_index}")


root = Tk()
root.title("Typing Speed Test")
root.minsize(width=400, height=150)
root.resizable(False, False)

cpm_label = Label(text="Corrected CPM: ", font=("Arial", 10))
cpm_label.grid(column=0, row=0)

wpm_label = Label(text="WPM: ", font=("Arial", 10))
wpm_label.grid(column=1, row=0)

time_left_label = Label(text="Time left: 60", font=("Arial", 10))
time_left_label.grid(column=2, row=0)

text_box = Text(height=3, width=38, font=("Arial", 14))
refresh_text_box()
text_box.grid(column=0, row=1, columnspan=3, pady=8)
text_box.config(state="disabled")

user_text = StringVar()
entry_text = Entry(font=("Arial", 12), textvariable=user_text)
entry_text.focus()
entry_text.grid(column=1, row=2, pady=8)

text_box.tag_config("green", background="green")
text_box.tag_config("red", foreground="red")
text_box.tag_config("white", foreground="white")
text_box.tag_config("blue", foreground="blue")

find_and_change(current_word)

root.bind(
    "<Key>",
    lambda e: start_countdown() if e.char.isalpha() and not countdown_started else None,
)


root.bind(
    "<Key>", lambda e: compare_letters(current_word) if e.char.isalpha() else None
)

# TODO: Need to solve backspace with one space + word color when using backspace
root.bind(
    "<KeyPress-BackSpace>",
    lambda e: backspace_action() if word_index > 0 and user_text.get() == "" else None,
)

root.bind(
    "<space>", lambda e: space_action() if not entry_text.get().isspace() else None
)

root.mainloop()
