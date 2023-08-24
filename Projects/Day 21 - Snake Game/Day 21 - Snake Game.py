from turtle import Screen
from snake import Snake, Food, Scoreboard
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
food = Food()
scoreboard = Scoreboard()

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

    # Detect collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.score_point()

    # Detect collision with wall
    if (
        snake.head.xcor() > 285 or snake.head.xcor() < -285
        or snake.head.ycor() > 285 or snake.head.ycor() < -285
    ):
        game_running = False
        scoreboard.game_over()

    # Detect collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_running = False
            scoreboard.game_over()

# Close the window when clicking on it
screen.exitonclick()
