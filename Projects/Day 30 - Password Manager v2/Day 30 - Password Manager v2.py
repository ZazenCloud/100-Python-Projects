import tkinter as tk
from tkinter import messagebox
from tkinter.constants import END
import random
import pyperclip
import json


def find_password():
    """
    If the website provided exists in the JSON file,
     displays email and password.
    """
    website = website_input.get()
    website_t = website.title()
    try:
        with open("password_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="No data file found!")
    else:
        if website_t == "List":
            # If the user entered "List", show all stored websites names
            keys = "\n".join(f"{key}" for key in data)
            messagebox.showinfo(title="Password List", message=keys)
        elif website_t in data:
            # If the website provided exists in the data,
            # show the corresponding email and password
            email = data[website_t]["email"]
            password = data[website_t]["password"]
            messagebox.showinfo(
                title=website_t,
                message=f"Email: {email} \nPassword: {password}"
            )
            # Copies the password to the clipboard
            pyperclip.copy(password)
        else:
            messagebox.showwarning(
                title="Warning", message="Data for this website was not found!"
            )


def generate_password():
    """
    Generates a random password and inserts it into the password_input field.
    """
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Randomly selects letters, symbols, and numbers to create a password
    password_list = [
        random.choice(letters) for _ in range(random.randint(10, 12))
    ]
    password_list += [
        random.choice(symbols) for _ in range(random.randint(2, 4))
    ]
    password_list += [
        random.choice(numbers) for _ in range(random.randint(2, 4))
    ]

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
    new_data = {
        website.title(): {
            "email": email,
            "password": password,
        }
    }

    if len(website) and len(email) and len(password):
        try:
            with open("password_data.json", "r") as file:
                # Reads old data
                data = json.load(file)
        except FileNotFoundError:
            with open("password_data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            if website.title() in data:
                # If the website already have credentials stored in the file,
                # asks the user to overwrite or not
                overwrite = messagebox.askyesno(
                    title="Warning",
                    message=f"A password for {website.title()} already exists!"
                            "\nOverwrite?"
                )
                if overwrite:
                    # Overwrites old data with new data
                    data.update(new_data)

                    with open("password_data.json", "w") as file:
                        # Saves overwritten data
                        json.dump(data, file, indent=4)
            else:
                # Updates old data with new data
                data.update(new_data)

                with open("password_data.json", "w") as file:
                    # Saves updated data
                    json.dump(data, file, indent=4)
        finally:
            # Clears the website_input field
            website_input.delete(0, END)
            # Clears the password_input field
            password_input.delete(0, END)
    else:
        # Shows a warning message if any of the fields are empty
        messagebox.showwarning(
            title="Warning", message="Don't leave any fields empty!"
        )


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
website_input = tk.Entry(width=28)
website_input.grid(row=1, column=1, padx=(0, 2))
website_input.focus()
email_input = tk.Entry(width=44)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "example@mail.com")
password_input = tk.Entry(width=28)
password_input.grid(row=3, column=1, padx=(0, 2))

# Buttons
search_button = tk.Button(text="Search", width=10, command=find_password)
search_button.grid(row=1, column=2, padx=(0, 14))
password_button = tk.Button(
    text="Generate", width=10, command=generate_password
)
password_button.grid(row=3, column=2, padx=(0, 14))
add_button = tk.Button(text="Add", width=37, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, padx=(1, 0))

# Canvas with logo image
canvas = tk.Canvas(width=200, height=200)
lock_img = tk.PhotoImage(file="pass_logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

window.mainloop()
