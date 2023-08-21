# from tkinter import Tk, Label, Entry, Text, END, StringVar, CHAR, WORD
from tkinter import *
import random
import time
import threading

word_list = ['table', 'book', 'camel', 'tree']

# Flag to indicate if the countdown has started
countdown_started = False

cpm_label = ''

wpm_label = ''



highest_cpm_label = ''

highest_wpm_label = ''

start_button = ''

entry_box = ''


def start_countdown():
    global countdown_started
    if not countdown_started:
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
        time_left_label.config(text=f'Time left: {str(remaining_time)}')
        # schedule the next update after 1 second
        time.sleep(1)
        update_label(end_time)
        
def update_label(end_time):
    # get the remaining time in seconds
    remaining_time = int(end_time - time.time())
    # check if the countdown is over
    if remaining_time <= 0:
        # set the label text to "Time's up!"
        label.config(text="Time's up!")
    
        


def start_test():
    pass


def stop_test():
    pass


def space_action():
    pass


def backspace_action():
    pass


# randomize list of 250 words

# start button

# clock
# focus on text

# every word (space), calculates score
# only counts if word is correct

# space goes back to the next word
# if no chars, just add a space

# press backspace delete chars
# if no chars, go back to the last word

ops = random.choices(word_list, k=10)

root = Tk()
root.title('Typing Speed Test')
root.minsize(width=500, height=500)

time_left_label = Label(text='Time left: 60')
time_left_label.pack()

text_box = Text(wrap=WORD)
text_box.insert(END, ops)
text_box.pack()

entry_text = Entry()
entry_text.focus()
entry_text.pack()

text_box.tag_config('green', background='green')
text_box.tag_add('green', '1.0', '1.end')

root.bind("<Key>", lambda e: start_countdown() if e.char.isalpha() else None)

root.mainloop()

####

# label = Label(text="This is old text")
# label.config(text="This is new text")

# button = Button(text="Click Me", command=action)

# entry.insert(END, string="Some text to begin with.")
