from tkinter import Tk, Button, Entry, filedialog
from PIL import Image, ImageDraw, ImageFont

filenames = None


def choose_files():
    global filenames
    filenames = filedialog.askopenfilenames(title="Select One or More Images:")


def add_watermark(image, watermark):
    opened_image = Image.open(image)

    # Get image size
    image_width, image_height = opened_image.size

    # Draw on image
    draw = ImageDraw.Draw(opened_image)

    # Font size
    font_size = int(image_width / 8)

    # For Windows, change font type to 'arial.ttf'
    font = ImageFont.truetype('arial.ttf', font_size)

    # Coordinates for where we want the image
    x, y = int(image_width / 2), int(image_height / 2)

    # Add the watermark
    draw.text(
        (x, y),
        watermark,
        font=font,
        fill='#FFF',
        stroke_width=5,
        stroke_fill='#222',
        anchor='ms'
    )

    # Show the new image
    opened_image.show()


def watermark_files():
    for file in filenames:
        add_watermark(file, text_entry.get())


root = Tk()

root.title("Image Watermarking")
root.minsize(250, 100)

choose_files = Button(text="Choose File(s)", command=choose_files)
choose_files.pack()

text_entry = Entry()
text_entry.pack()

process_button = Button(text="Watermark File(s)", command=watermark_files)
process_button.pack()

root.mainloop()
