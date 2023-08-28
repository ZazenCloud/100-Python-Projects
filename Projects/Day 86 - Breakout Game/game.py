from turtle import Turtle

STARTING_POSITION = (0, -280)
BRICKS_COLORS = ["red", "orange", "green", "yellow"]


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__("square")
        self.color("blue")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def go_right(self):
        new_x = self.xcor() + 20
        self.goto(new_x, self.ycor())

    def go_left(self):
        new_x = self.xcor() - 20
        self.goto(new_x, self.ycor())

    def go_to_start(self):
        self.goto(STARTING_POSITION)


class Ball(Turtle):

    def __init__(self):
        super().__init__("square")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1
        self.move_speed *= 0.9

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.1
        self.bounce_y()


class Bricks(Turtle):

    def __init__(self, position, color, health):
        # inherit from Turtle class and set shape to square
        super().__init__("square")
        # set color according to parameter
        self.color(color)
        # stretch width and length to 5 and 1
        self.shapesize(stretch_wid=5, stretch_len=1)
        # lift pen up from screen
        self.penup()
        # move to position according to parameter
        self.goto(position)
        # set health according to parameter
        self.health = health

    def got_hit(self):
        self.health -= 1
        # If health is 0, destroy brick
        if self.health == 0:
            self.destroy()

    def destroy(self):
        # Erase brick from screen
        self.clear()
        # Hide brick from view
        self.hideturtle()


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.points = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(100, 200)
        self.write(
            self.points, align="center", font=("Courier", "80", "normal")
        )

    def points(self):
        self.points += 1
        self.update_scoreboard()
