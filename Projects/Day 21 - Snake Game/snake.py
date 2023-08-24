from turtle import Turtle
import random
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
FONT = ("Arial", 24, "normal")


class Snake:

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        # Create the initial snake segments
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        # Create a new white square segment
        new_segment = Turtle("square")
        new_segment.color("white")
        # Lift the pen to avoid drawing lines
        new_segment.penup()
        new_segment.goto(position)
        # Add the segment to the list of segments
        self.segments.append(new_segment)

    def extend(self):
        # Add a new segment to the snake
        self.add_segment(self.segments[-1].position())

    def move(self):
        # Move the snake segments forward
        for seg_num in range(len(self.segments) - 1, 0, -1):
            # Get the x-coordinate of the previous segment
            new_x = self.segments[seg_num - 1].xcor()
            # Get the y-coordinate of the previous segment
            new_y = self.segments[seg_num - 1].ycor()
            # Move the current segment to the new coordinates
            self.segments[seg_num].goto(new_x, new_y)
        # Move the head segment forward by the specified distance
        self.head.forward(MOVE_DISTANCE)

    # Change the snake's heading (if it's not a opposite direction)
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        # Move the food to a random position
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.points = -1
        self.color("white")
        self.penup()
        self.goto(0, 260)
        self.hideturtle()
        self.score_point()

    def score_point(self):
        # Increase the score by 1 and display it on the screen
        self.points += 1
        self.clear()
        self.write(f"Score: {self.points}", align="center", font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=FONT)
