from turtle import Screen
from pong import Paddle, Ball, Scoreboard
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong!")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

# Enable listening for keyboard input
screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

game_running = True

while game_running:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect collision with the wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with the right paddle
    if (
        ball.distance(r_paddle) < 40 and ball.xcor() > 320
        or ball.distance(l_paddle) < 40 and ball.xcor() < -320
    ):
        ball.bounce_x()

    # Detect when right paddle misses
    if ball.xcor() > 380:
        # Reset the ball position to the center
        ball.reset_position()
        scoreboard.l_point()

    # Detect when left paddle misses
    if ball.xcor() < -380:
        # Reset the ball position to the center
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()
