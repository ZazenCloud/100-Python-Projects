# Solving the procedural generated maze at Reeborg's World
# https://reeborg.ca/reeborg.html?lang=en&mode=python&menu=worlds%2Fmenus%2Freeborg_intro_en.json&name=Maze&url=worlds%2Ftutorial_en%2Fmaze1.json

def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
# A common approach to solve an unknown maze is to follow along the right wall/edge

num_turns = 0 # Check the numbers of right turns to avoid infinite square movement

while not at_goal():
        if right_is_clear() and num_turns % 4 != 3:
            turn_right()
            move()
            num_turns += 1
        elif front_is_clear():
            move()
            num_turns = 0
        else:
            turn_left()
            num_turns = 0