import turtle
import pandas
# Download usa_states_img.gif and usa_states.csv
# (located on this repository) and move them to same folder of this file

# Create a turtle screen
screen = turtle.Screen()
screen.title("U.S. States Game")

# Load U.S. states map image
image = "usa_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# Read the data of U.S. states from a CSV file
data = pandas.read_csv("usa_states.csv")
# Transform the state name data into a list
state_list = data.state.to_list()
correct_guesses = []

# Start the game loop until all states are guessed correctly or the user exits
while len(correct_guesses) < len(state_list):
    # Ask the user to guess a state name
    answer = screen.textinput(title=f"{len(correct_guesses)}/{len(state_list)}",
                              prompt="Guess a State name!").title()
    if answer == "Exit":
        states_to_learn = []
        # Find the states that haven't been correctly guessed
        for state in state_list:
            if state not in correct_guesses:
                states_to_learn.append(state)
        # Save the states to learn in a CSV file
        df = pandas.DataFrame(states_to_learn)
        df.to_csv("states_to_learn.csv")
        break
    # Check if the guessed state name is correct
    if answer in state_list:
        correct_guesses.append(answer)
        state_pos = data[data.state == answer]
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.speed("fastest")
        t.goto(int(state_pos.x), int(state_pos.y))
        t.write(answer)
