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
from PIL import Image, ImageDraw, ImageFont

filenames = None
logo = None


def choose_files():
    global filenames
    filenames = filedialog.askopenfilenames(title="Select One or More Images:")


def choose_logo():
    global filenames
    filenames = filedialog.askopenfilename(title="Select a Logo:")


def checkbutton_text_used():
    checkbutton_image.toggle()
    text_entry.config(state="normal")
    choose_logo_button.config(state="disabled")


def checkbutton_image_used():
    checkbutton_text.toggle()
    choose_logo_button.config(state="normal")
    text_entry.config(state="disabled")


def radio_used():
    print(radio_state.get())


def set_watermark_position(position, image_width, image_height):
    """Transforms the selected position in X/Y coordinates."""

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


def add_watermark(image, watermark, checked_state_text, radio_state, opacity):
    opened_image = Image.open(image).convert("RGBA")

    # Get image size
    image_width, image_height = opened_image.size

    # Create transparent layer
    transparent_image = Image.new(
        "RGBA", (image_width, image_height), (255, 255, 255, 0)
    )

    # Draw on transparent layer
    draw = ImageDraw.Draw(transparent_image)

    # Coordinates for where we want the watermark
    x, y, anchor = set_watermark_position(radio_state, image_width, image_height)

    if checked_state_text:
        # Font size
        font_size = 100

        # For Windows, change font type to 'arial.ttf'
        font = ImageFont.truetype("arial.ttf", font_size)

        # Add the watermark
        draw.text(
            (x, y),
            watermark,
            font=font,
            fill=(255, 255, 255, int(255 * (opacity / 100))),
            stroke_width=5,
            stroke_fill=(0, 0, 0, int(255 * (opacity / 100))),
            anchor=anchor,
        )
    else:
        pass

    combined_image = Image.alpha_composite(
        opened_image.convert("RGBA"), transparent_image
    )

    # combined_image.save("abc.png", "PNG")

    # Show the new image
    combined_image.show()


def watermark_files():
    for file in filenames:
        add_watermark(
            file,
            text_entry.get(),
            checked_state_text.get(),
            radio_state.get(),
            opacity_state.get(),
        )


root = Tk()

root.title("Image Watermarking")
root.minsize(250, 100)

files_label = Label(text="File(s) to Watermark")
files_label.pack()

choose_files_button = Button(text="Choose File(s)", command=choose_files)
choose_files_button.pack()

position_label = Label(text="Position")
position_label.pack()


# Variable to hold on to which radio button value is checked
radio_state = IntVar(value=4)

radiobutton1 = Radiobutton(
    text="Top Left", value=1, variable=radio_state, command=radio_used
)
radiobutton2 = Radiobutton(
    text="Top Center", value=2, variable=radio_state, command=radio_used
)
radiobutton3 = Radiobutton(
    text="Top Right", value=3, variable=radio_state, command=radio_used
)
radiobutton4 = Radiobutton(
    text="Center", value=4, variable=radio_state, command=radio_used
)
radiobutton5 = Radiobutton(
    text="Bottom Left", value=5, variable=radio_state, command=radio_used
)
radiobutton6 = Radiobutton(
    text="Bottom Center", value=6, variable=radio_state, command=radio_used
)
radiobutton7 = Radiobutton(
    text="Bottom Right", value=7, variable=radio_state, command=radio_used
)
radiobutton1.pack()
radiobutton2.pack()
radiobutton3.pack()
radiobutton4.pack()
radiobutton5.pack()
radiobutton6.pack()
radiobutton7.pack()


# Variable to hold on to checked state, 0 is off, 1 is on
checked_state_text = IntVar(value=1)
checkbutton_text = Checkbutton(
    text="Text?", variable=checked_state_text, command=checkbutton_text_used
)
checked_state_text.get()
checkbutton_text.pack()

text_entry = Entry()
text_entry.pack()


# Variable to hold on to checked state, 0 is off, 1 is on
checked_state_image = IntVar()
checkbutton_image = Checkbutton(
    text="Image?", variable=checked_state_image, command=checkbutton_image_used
)
checked_state_image.get()
checkbutton_image.pack()

choose_logo_button = Button(text="Choose Logo", state="disabled", command=choose_logo)
choose_logo_button.pack()


watermark_size_label = Label(text="Watermark Size")
watermark_size_label.pack()

size_state = IntVar(value=3)
watermark_size = Scale(from_=1, to=5, orient="horizontal", variable=size_state)
watermark_size.pack()


watermark_opacity_label = Label(text="Watermark Opacity")
watermark_opacity_label.pack()

opacity_state = IntVar(value=55)
watermark_opacity = Scale(
    from_=10, to=100, orient="horizontal", variable=opacity_state, resolution=5
)
watermark_opacity.pack()

process_button = Button(text="Watermark File(s)", command=watermark_files)
process_button.pack()

checked_state_save = IntVar(value=0)
checkbutton_save = Checkbutton(text="Save to Disk?", variable=checked_state_save)
# checked_state_text.get()
checkbutton_save.pack()

checked_state_show = IntVar(value=1)
checkbutton_show = Checkbutton(text="Show After?", variable=checked_state_show)
# checked_state_text.get()
checkbutton_show.pack()

root.mainloop()
