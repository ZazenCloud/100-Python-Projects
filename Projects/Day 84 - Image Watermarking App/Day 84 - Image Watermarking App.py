from tkinter import (
    Tk,
    Button,
    Entry,
    filedialog,
    IntVar,
    Checkbutton,
    Radiobutton,
    Label,
    Scale,
)
import tkinter.messagebox as mb
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

filenames = None
logo = None


def choose_files():
    """Choose one or more image files from the file dialog."""
    global filenames
    filenames = filedialog.askopenfilenames(
        title="Select One or More Images:",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")],
    )


def choose_logo():
    """Choose a logo file from the file dialog."""
    global logo
    logo = filedialog.askopenfilename(
        title="Select a Logo:", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
    )


def checkbutton_text_used():
    """
    Handles the checkbutton for text watermark option.\n
    When text or image is selected, the other option is disabled.
    """
    checkbutton_image.toggle()

    # If "Text?" is checked
    if checked_state_text.get() == 1:
        text_entry.config(state="normal")
        choose_logo_button.config(state="disabled")
    # If "Image?" is checked
    elif checked_state_image.get() == 1:
        choose_logo_button.config(state="normal")
        text_entry.config(state="disabled")


def checkbutton_image_used():
    """
    Handles the checkbutton for image watermark option.\n
    When text or image is selected, the other option is disabled.
    """
    checkbutton_text.toggle()

    # If "Image?" is checked
    if checked_state_image.get() == 1:
        choose_logo_button.config(state="normal")
        text_entry.config(state="disabled")
    # If "Text?" is checked
    elif checked_state_text.get() == 1:
        text_entry.config(state="normal")
        choose_logo_button.config(state="disabled")


def checkbutton_save_used():
    """
    Handles the checkbutton for save option.\n
    When save is enabled, show is optional.\n
    When save is disabled, show is mandatory.
    """
    if checked_state_save.get() == 0:
        checkbutton_show.config(state="disabled")
        checked_state_show.set(1)
    else:
        checkbutton_show.config(state="normal")


def set_watermark_position(position, image_width, image_height):
    """Sets watermark position based on user's choice."""

    # Top Left
    if position == 1:
        x = int(image_width / 32)
        y = int(image_height / 12)
        return x, y, "lm"

    # Top Center
    elif position == 2:
        x = int(image_width / 2)
        y = int(image_height / 12)
        return x, y, "mm"

    # Top Right
    elif position == 3:
        x = int(image_width) - int(image_width / 32)
        y = int(image_height / 12)
        return x, y, "rm"

    # Center
    elif position == 4:
        x = int(image_width / 2)
        y = int(image_height / 2)
        return x, y, "mm"

    # Bottom Left
    elif position == 5:
        x = int(image_width / 32)
        y = int(image_height) - int(image_height / 12)
        return x, y, "lm"

    # Bottom Center
    elif position == 6:
        x = int(image_width / 2)
        y = int(image_height) - int(image_height / 12)
        return x, y, "mm"

    # Bottom Right
    else:
        x = int(image_width) - int(image_width / 32)
        y = int(image_height) - int(image_height / 12)
        return x, y, "rm"


def add_watermark(
    image,
    text_watermark,
    logo_watermark,
    checked_state_text,
    radio_state,
    size,
    opacity,
    checked_state_save,
    checked_state_show,
):
    """Adds watermark to an image file."""

    # Open the image file and convert it to RGBA mode
    opened_image = Image.open(image).convert("RGBA")

    # Get image size
    image_width, image_height = opened_image.size

    # Create a transparent layer with the same size as the original image
    transparent_image = Image.new(
        "RGBA", (image_width, image_height), (255, 255, 255, 0)
    )

    # Coordinates and alignment of the watermark, based on user's choice
    x, y, anchor = set_watermark_position(radio_state, image_width, image_height)

    if checked_state_text:
        # Font size
        font_size = int(image_height / 32) * size

        # Font type
        font = ImageFont.truetype("arial", font_size)

        if os.name == "nt":
            # For Windows, change font type to 'arial.ttf'
            font = ImageFont.truetype("arial.ttf", font_size)

        # Create a drawing object to draw on the transparent image
        draw = ImageDraw.Draw(transparent_image)

        # Add the watermark
        draw.text(
            (x, y),
            text_watermark,
            font=font,
            fill=(255, 255, 255, int(255 * (opacity / 100))),
            stroke_width=5,
            stroke_fill=(0, 0, 0, int(255 * (opacity / 100))),
            anchor=anchor,
        )

    # If the text watermark option is not selected, use the image watermark option
    else:
        # If no logo is chosen, call the choose_logo function
        # to prompt the user to choose a logo file
        while not logo:
            choose_logo()

        logo_watermark = logo

        # Open the logo file and convert it to RGBA mode
        logo_watermark = Image.open(logo_watermark).convert("RGBA")

        # Get the alpha channel of the logo image
        logo_alpha = logo_watermark.getchannel("A")

        # Adjust the alpha channel according to the opacity scale
        new_logo_alpha = logo_alpha.point(
            lambda i: int((opacity / 100) * 255) if i > 0 else 0
        )

        # Replace the alpha channel of the logo image with the adjusted one
        logo_watermark.putalpha(new_logo_alpha)

        # Get the width and height of the logo image
        logo_width, logo_height = logo_watermark.size

        # Calculate the new logo size based on the logo width and height and the size scale
        new_logo_size = (int(logo_width / 32) * size, int(logo_height / 32) * size)

        # Resize the logo image using Lanczos filter
        resized_logo = logo_watermark.resize(new_logo_size, Image.LANCZOS)

        # Calculate the paste coordinates for the logo image
        paste_logo_x = x - resized_logo.size[0] // 2
        paste_logo_y = y - resized_logo.size[1] // 2

        # Adjust the paste coordinates for different positions #

        # Top positions
        if radio_state < 4:
            paste_logo_y += resized_logo.size[1] // 4
        # Bottom positions
        elif radio_state > 4:
            paste_logo_y -= resized_logo.size[1] // 3

        # Left positions
        if radio_state == 1 or radio_state == 5:
            paste_logo_x += resized_logo.size[0] // 2
        # Right positions
        elif radio_state == 3 or radio_state == 7:
            paste_logo_x -= resized_logo.size[0] // 2

        # Paste the resized logo on the transparent image
        transparent_image.paste(resized_logo, (paste_logo_x, paste_logo_y))

    # Combine the original image and the transparent image
    combined_image = Image.alpha_composite(
        opened_image.convert("RGBA"), transparent_image
    )

    # Check if the save option is selected
    if checked_state_save:
        # Get the current date and time as a string
        now = datetime.now()
        now_string = now.strftime("%Y-%m-%d at %H.%M.%S")

        # Get the image name without the extension
        image_name_without_extension = os.path.splitext(image)[0]

        # Save the combined image as a PNG file with a
        # "_watermark" suffix and the current date and time
        combined_image.save(
            image_name_without_extension + "_watermarked " + now_string + ".png", "PNG"
        )

    # Check if the show option is selected
    if checked_state_show:
        # Show the combined image in a new window
        combined_image.show()


def watermark_files():
    "Watermark one or more files."
    # Check if any file is chosen
    if not filenames:
        # If not, show a warning message and prompt the user to choose files
        mb.showwarning(
            title="Warning!", message="Select at least one file to watermark"
        )
        choose_files()

        # If still no file is chosen, return from the function
        if not filenames:
            return

    # Loop through each file in the filenames tuple
    for file in filenames:
        # Watermark the file
        add_watermark(
            file,
            text_entry.get(),
            logo,
            checked_state_text.get(),
            radio_state.get(),
            size_state.get(),
            opacity_state.get(),
            checked_state_save.get(),
            checked_state_show.get(),
        )


root = Tk()

root.title("Image Watermarking")
root.minsize(300, 300)
root.resizable(False, False)

# File(s) label
files_label = Label(text="File(s) to Watermark")
files_label.grid(column=2, row=0, pady=5)

# Choose File(s) button
choose_files_button = Button(text="Choose File(s)", command=choose_files)
choose_files_button.grid(column=2, row=1, pady=10)

# Position label
position_label = Label(text="Position")
position_label.grid(column=0, row=3, sticky="w", padx=3)

# Variable to hold on to which radio button value is checked
radio_state = IntVar(value=4)

# Radio buttons (Watermark position)
radiobutton1 = Radiobutton(text="Top Left", value=1, variable=radio_state)
radiobutton2 = Radiobutton(text="Top Center", value=2, variable=radio_state)
radiobutton3 = Radiobutton(text="Top Right", value=3, variable=radio_state)
radiobutton4 = Radiobutton(text="Center", value=4, variable=radio_state)
radiobutton5 = Radiobutton(text="Bottom Left", value=5, variable=radio_state)
radiobutton6 = Radiobutton(text="Bottom Center", value=6, variable=radio_state)
radiobutton7 = Radiobutton(text="Bottom Right", value=7, variable=radio_state)
radiobutton1.grid(column=0, row=4, sticky="w", pady=8)
radiobutton2.grid(column=0, row=5, sticky="w", pady=8)
radiobutton3.grid(column=0, row=6, sticky="w", pady=8)
radiobutton4.grid(column=0, row=7, sticky="w", pady=8)
radiobutton5.grid(column=0, row=8, sticky="w", pady=8)
radiobutton6.grid(column=0, row=9, sticky="w", pady=8)
radiobutton7.grid(column=0, row=10, sticky="w", pady=8)

# Variable to check if the text watermark option is checked
checked_state_text = IntVar(value=1)

# "Text?" checkbutton
checkbutton_text = Checkbutton(
    text="Text?", variable=checked_state_text, command=checkbutton_text_used
)
checkbutton_text.grid(column=2, row=3, pady=10)

# User text input
text_entry = Entry()
text_entry.grid(column=2, row=4, padx=5)

# Variable to check if the image watermark option is checked
checked_state_image = IntVar()

# "Image?" checkbutton
checkbutton_image = Checkbutton(
    text="Image?", variable=checked_state_image, command=checkbutton_image_used
)
checkbutton_image.grid(column=2, row=5)

# Choose Logo button
choose_logo_button = Button(text="Choose Logo", state="disabled", command=choose_logo)
choose_logo_button.grid(column=2, row=6)

# Watermark size label
watermark_size_label = Label(text="Watermark Size")
watermark_size_label.grid(column=1, row=7)

# Variable to hold the value of the watermark size scale
size_state = IntVar(value=3)

# Size scale
watermark_size = Scale(from_=1, to=5, orient="horizontal", variable=size_state)
watermark_size.grid(column=1, row=8, padx=8)

# Watermark opacity label
watermark_opacity_label = Label(text="Watermark Opacity")
watermark_opacity_label.grid(column=1, row=9)

# Variable to hold the value of the watermark opacity scale
opacity_state = IntVar(value=55)

# Opacity scale
watermark_opacity = Scale(
    from_=10, to=100, orient="horizontal", variable=opacity_state, resolution=5
)
watermark_opacity.grid(column=1, row=10)

# Watermark File(s) button
process_button = Button(text="Watermark File(s)", command=watermark_files)
process_button.grid(column=2, row=8, padx=12)

# Variable to check if the save option is checked
checked_state_save = IntVar(value=0)

# "Save to Disk?" checkbutton
checkbutton_save = Checkbutton(
    text="Save to Disk?", variable=checked_state_save, command=checkbutton_save_used
)
checkbutton_save.grid(column=2, row=9)

# Variable to check if the show option is checked
checked_state_show = IntVar(value=1)

# "Show After?" checkbutton
checkbutton_show = Checkbutton(text="Show After?", variable=checked_state_show)
checkbutton_show.config(state="disabled")
checkbutton_show.grid(column=2, row=10)

root.mainloop()
