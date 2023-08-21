import turtle
import random

# Created via the colorgram.py module
color_list = [(35, 118, 151), (38, 167, 184), (99, 180, 197), (102, 195, 170),
              (51, 179, 166), (182, 226, 207), (149, 215, 198), (240, 223, 187),
              (134, 80, 101), (232, 120, 129), (216, 145, 124), (219, 72, 85),
              (252, 156, 146), (23, 60, 116), (11, 53, 106), (137, 214, 219),
              (106, 110, 171), (65, 122, 112), (231, 73, 64), (222, 208, 136),
              (183, 222, 228), (197, 15, 30), (133, 91, 78), (248, 142, 146),
              (236, 218, 225), (12, 84, 108), (71, 41, 50), (251, 8, 23),
              (203, 15, 12), (140, 139, 97)]
# Set the color mode to RGB
turtle.colormode(255)
# Create a turtle named "artist"
artist = turtle.Turtle()
# Set the drawing speed
artist.speed("fastest")
# Lift the pen up to prevent drawing lines
artist.penup()
# Hide the turtle icon
artist.hideturtle()
# Set the start position
artist.setheading(225)
artist.forward(300)
artist.setheading(0)


for _ in range(10):
    for _ in range(10):
        # Draw a dot with a size of 20 units and a random color from the color_list
        artist.dot(20, random.choice(color_list))
        artist.forward(50)
    artist.left(90)
    artist.forward(50)
    artist.left(90)
    artist.forward(500)
    artist.left(180)


screen = turtle.Screen()
# Close the screen when clicked
screen.exitonclick()
