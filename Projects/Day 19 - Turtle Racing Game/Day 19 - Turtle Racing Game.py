from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(
  title="Make your bet!",
  prompt=
  "Which turtle will win the race? \n\nChoose a color:\nBlack - Red - Green - Blue"
)
print(user_bet)
colors = ["blue", "green", "red", "black"]
y_position = [-100, -35, 35, 100]
all_turtles = []
game_running = False

for turtle_index in range(4):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_position[turtle_index])
    all_turtles.append(new_turtle)

if user_bet:
    game_running = True

while game_running:
    for turtle in all_turtles:
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

        if turtle.xcor() > 235:
            game_running = False
            winning_turtle = turtle.pencolor()
            if winning_turtle == user_bet.lower():
                print(f"You've won! The {winning_turtle} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_turtle} turtle is the winner!")

screen.exitonclick()
