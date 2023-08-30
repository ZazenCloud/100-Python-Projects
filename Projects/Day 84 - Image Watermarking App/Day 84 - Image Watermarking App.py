from tkinter import Tk, Button, Entry, filedialog, IntVar, Checkbutton, Radiobutton, Label
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
    text_entry.config(state='normal')
    choose_logo_button.config(state='disabled')


def checkbutton_image_used():
    checkbutton_text.toggle()
    choose_logo_button.config(state='normal')
    text_entry.config(state='disabled')


def radio_used():
    print(radio_state.get())


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

files_label = Label(text="File(s) to Watermark:")
files_label.pack()

choose_files_button = Button(text="Choose File(s)", command=choose_files)
choose_files_button.pack()

position_label = Label(text="Position:")
position_label.pack()


#Variable to hold on to which radio button value is checked
radio_state = IntVar(value=4)

radiobutton1 = Radiobutton(text="Top Left", value=1, variable=radio_state, command=radio_used)
radiobutton2 = Radiobutton(text="Top Center", value=2, variable=radio_state, command=radio_used)
radiobutton3 = Radiobutton(text="Top Right", value=3, variable=radio_state, command=radio_used)
radiobutton4 = Radiobutton(text="Center", value=4, variable=radio_state, command=radio_used)
radiobutton5 = Radiobutton(text="Bottom Left", value=5, variable=radio_state, command=radio_used)
radiobutton6 = Radiobutton(text="Bottom Center", value=6, variable=radio_state, command=radio_used)
radiobutton7 = Radiobutton(text="Bottom Right", value=7, variable=radio_state, command=radio_used)
radiobutton1.pack()
radiobutton2.pack()
radiobutton3.pack()
radiobutton4.pack()
radiobutton5.pack()
radiobutton6.pack()
radiobutton7.pack()


# Variable to hold on to checked state, 0 is off, 1 is on
checked_state_text = IntVar(value=1)
checkbutton_text = Checkbutton(text="Text?", variable=checked_state_text, command=checkbutton_text_used)
checked_state_text.get()
checkbutton_text.pack()

text_entry = Entry()
text_entry.pack()


# Variable to hold on to checked state, 0 is off, 1 is on
checked_state_image = IntVar()
checkbutton_image = Checkbutton(text="Image?", variable=checked_state_image, command=checkbutton_image_used)
checked_state_image.get()
checkbutton_image.pack()

choose_logo_button = Button(text="Choose Logo", state='disabled', command=choose_logo)
choose_logo_button.pack()

process_button = Button(text="Watermark File(s)", command=watermark_files)
process_button.pack()

root.mainloop()
