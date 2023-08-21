import time
from turtle import Screen
# Download turtle_crossing.py (located on this repository) and move it to same folder of this file
from turtle_crossing import Player, Scoreboard, CarManager

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()
# Turn off the automatic screen updates
scoreboard.score()

screen.listen()
screen.onkeypress(player.move_up, "Up")
screen.onkeypress(player.move_down, "Down")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    # Create a new car
    car_manager.create_car()
    # Move all the cars
    car_manager.move_cars()

    # Detect collision with car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    # Detect successful crossing
    if player.is_at_finish_line():
        # Reset the player's position
        player.go_to_start()
        # Increase the car speed
        car_manager.level_up()
        # Update the score
        scoreboard.score()

screen.exitonclick()
