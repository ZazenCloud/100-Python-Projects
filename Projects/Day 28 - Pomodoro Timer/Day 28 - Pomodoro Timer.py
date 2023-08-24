import tkinter as tk

# Constants for colors, fonts, and time intervals
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


def reset_timer():
    '''Resets the timer and other UI elements'''
    # Cancels the timer event
    window.after_cancel(timer)
    # Resets the timer label text to "Timer" and sets the color to green
    timer_label.config(text="Timer", fg=GREEN)
    # Resets the clock display in the canvas to "00:00"
    canvas.itemconfig(clock, text="00:00")
    # Clears the check mark label
    check_mark_label.config(text="")
    global reps
    reps = 0


def start_timer():
    '''Starts the timer and manages work and break sections'''
    global reps
    reps += 1
    work_section = WORK_MIN * 60
    short_break_section = SHORT_BREAK_MIN * 60
    long_break_section = LONG_BREAK_MIN * 60

    # For odd sessions -> work
    if reps % 2 != 0:
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_section)
    # For the 4th break (after 4 work session) -> long break
    elif reps % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        count_down(long_break_section)
    # For even sessions, other then % 8 == 0 -> short break
    else:
        timer_label.config(text="Break", fg=PINK)
        count_down(short_break_section)


def count_down(count):
    '''Handles the countdown and updates the UI'''
    # Divides the count by 60 to obtain minutes and seconds
    time_tuple = divmod(count, 60)
    minutes = time_tuple[0]
    seconds = time_tuple[1]
    # Adds a leading zero to the seconds if it's less than 10
    if seconds < 10:
        seconds = f"0{seconds}"

    canvas.itemconfig(clock, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        # Sets up a callback to execute count_down() after 1000 milliseconds
        # With count decremented by 1
        timer = window.after(1000, count_down, count - 1)
    else:
        # Calls the start_timer() function to move
        # to the next section (work or break)
        start_timer()
        # Add 1 check mark after a work session
        check_count = divmod(reps, 2)
        check_mark_label.config(text=f"{check_count[0]*'✓'}")


# Main window
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# Buttons
start_button = tk.Button(
    text="Start", highlightthickness=0, command=start_timer
)
start_button.grid(row=2, column=0)
reset_button = tk.Button(
    text="Reset", highlightthickness=0, command=reset_timer
)
reset_button.grid(row=2, column=2)
# Labels
timer_label = tk.Label(
    text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold")
)
timer_label.grid(row=0, column=1)
check_mark_label = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check_mark_label.grid(row=3, column=1)
# Image + timer
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
clock = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(row=1, column=1)

window.mainloop()
