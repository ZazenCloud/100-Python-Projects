import tkinter as tk
from tkinter import messagebox
from tkinter.constants import END
import random
import pyperclip
# Download pass_logo.png (located on this repository)
# And move it to same folder of this file


def generate_password():
    """Generates a random password and inserts it into the password_input field"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Randomly selects letters, symbols, and numbers to create a password
    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    # Shuffles the password list
    random.shuffle(password_list)

    password = ""
    for char in password_list:
        # Concatenates the characters to form the final password
        password += char

    # Clears the password_input field
    password_input.delete(0, END)
    # Inserts the generated password into the password_input field
    password_input.insert(0, password)
    # Copies the generated password to the clipboard
    pyperclip.copy(password)


def save_data():
    """Saves the website, email, and password data to a file"""
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    if len(website) and len(email) and len(password):
        # Asks for confirmation to save the data
        save_it = messagebox.askokcancel(title=website, message=f"These are the details provided: \n"
                                         f"\nEmail: {email} \nPassword: {password} \n\nSave it?")
        if save_it:
            # Appends the data to a file
            with open("password_data.txt", "a") as file:
                file.write(f"{website} | {email} | {password}\n")
            # Clears the website_input field
            website_input.delete(0, END)
            # Clears the password_input field
            password_input.delete(0, END)
    else:
        # Shows a warning message if any of the fields are empty
        messagebox.showwarning(title="Warning", message="Don't leave any fields empty!")


window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0, padx=(0, 5))

# Inputs
website_input = tk.Entry(width=44)
website_input.grid(row=1, column=1, columnspan=2)
website_input.focus()
email_input = tk.Entry(width=44)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "example@mail.com")
password_input = tk.Entry(width=28)
password_input.grid(row=3, column=1, padx=(0, 2))

# Buttons
password_button = tk.Button(text="Generate", width=10, command=generate_password)
password_button.grid(row=3, column=2, padx=(0, 14))
add_button = tk.Button(text="Add", width=37, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, padx=(1, 0))

# Canvas with logo image
canvas = tk.Canvas(width=200, height=200)
lock_img = tk.PhotoImage(file="pass_logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

window.mainloop()
