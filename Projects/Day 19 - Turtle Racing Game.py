from turtle import Turtle, Screen

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet!", prompt="Which turtle will win the race? \nEnter a color: ")
print(user_bet)
colors = ["black", "red", "green", "blue"]
    

black_turtle = Turtle(shape="turtle")
black_turtle.penup()
black_turtle.goto(x=-230, y=90)

red_turtle = Turtle(shape="turtle")
red_turtle.penup()
red_turtle.goto(x=-230, y=30)

green_turtle = Turtle(shape="turtle")
green_turtle.penup()
green_turtle.goto(x=-230, y=-30)

blue_turtle = Turtle(shape="turtle")
blue_turtle.penup()
blue_turtle.goto(x=-230, y=-90)

screen.exitonclick()
