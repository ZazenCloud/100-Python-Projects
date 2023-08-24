from turtle import Turtle
import random

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):

    def __init__(self):
        super().__init__("turtle")
        self.penup()
        self.setheading(90)
        self.go_to_start()

    def go_to_start(self):
        # Move the player to the starting position
        self.goto(STARTING_POSITION)

    def move_up(self):
        self.forward(MOVE_DISTANCE)

    def move_down(self):
        self.backward(MOVE_DISTANCE)

    def is_at_finish_line(self):
        # Check if the player has reached the finish line
        if self.ycor() > FINISH_LINE_Y:
            return True
        else:
            return False


FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-200, 250)
        self.current_level = 0

    def score(self):
        # Update the scoreboard with the current level
        self.clear()
        self.current_level += 1
        self.write(f"Level: {self.current_level}", align="center", font=FONT)

    def game_over(self):
        # Display the game over message
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=FONT)


COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 5


class CarManager(Turtle):

    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(self):
        # Randomly create a car (1 in 6 chance)
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            new_car = Turtle("square")
            new_car.penup()
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-250, 250)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self):
        # Move all the cars from right to left
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        # Increase the car speed for the next level
        self.car_speed += MOVE_INCREMENT
