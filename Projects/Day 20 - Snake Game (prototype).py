from turtle import Screen
# Download snake_proto.py (located on this repository) and move it to same folder of this file
from snake_proto import Snake
import time

screen = Screen()
# Set the screen dimensions
screen.setup(width=600, height=600)
# Set the background color
screen.bgcolor("black")
# Set the window title
screen.title("Snake Game")
# Turn off animation updates
screen.tracer(0)

snake = Snake()

# Enable listening for keyboard input
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_running = True

while game_running:
    # Update the screen
    screen.update()
    time.sleep(0.1)

    snake.move()

# Close the window when clicking on it
screen.exitonclick()
