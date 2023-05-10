# Import the random module
import random

# Import os for the clear() function
import os

# Import game data
# Download higherlower_data.py from this repository
from higherlower_data import data

# Art
logo = """
    __  ___       __             
   / / / (_)___ _/ /_  ___  _____
  / /_/ / / __ `/ __ \/ _ \/ ___/
 / __  / / /_/ / / / /  __/ /    
/_/ ///_/\__, /_/ /_/\___/_/     
   / /  /____/_      _____  _____
  / /   / __ \ | /| / / _ \/ ___/
 / /___/ /_/ / |/ |/ /  __/ /    
/_____/\____/|__/|__/\___/_/     
"""

vs = """
 _    __    
| |  / /____
| | / / ___/
| |/ (__  ) 
|___/____(_)
"""

def clear():
    ''' Clears the console.'''
    os.system('cls' if os.name == 'nt' else 'clear') # 'cls' for Windows / 'clear' for Unix-based systems

def check_guess(guess, followers_A, followers_B):
    '''Compares the follower count of two items and return True if user's guess is right.'''
    if followers_A > followers_B:
        return guess == 'A'
    else:
        return guess == 'B'

print(logo)    
score = 0
end_game = False
item_B = random.choice(data) # Choose a random item to start the game

# Loop until game ends
while not end_game:
    # Set the current item_A to the previous item_B
    item_A = item_B
    # Choose a new item_B
    item_B = random.choice(data)
    # Make sure item_A and item_B are not the same
    while item_A == item_B:
        item_B = random.choice(data)
    
    # Print the two items and ask user to guess            
    print(f"\nA: {item_A['name']}, a {item_A['description']}, from {item_A['country']}.")
    print(vs)
    print(f"\nB: {item_B['name']}, a {item_B['description']}, from {item_B['country']}.")
    guess = input("\nWho has more followers? Type 'A' or 'B': ").upper()
    
    # Get the number of followers for item_A and item_B
    followers_A = item_A['follower_count']
    followers_B = item_B['follower_count']
    
    # Check if the user's guess is correct
    correct_guess = check_guess(guess, followers_A, followers_B)
    
    clear()
    print(logo)
    if correct_guess:
        score += 1
        print(f'\nYou got it! Current score: {score}.')
    else:
        print(f'\nWrong. You lose! \n\nFinal score: {score}.')
        end_game = True
