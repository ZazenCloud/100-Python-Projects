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

print(logo)

def compare_items(choice, item_A, item_B, score, end_game):
    '''Compares the follower count of two random items and updates the score based on the user's choice.'''
    followers_A = item_A['follower_count']
    followers_B = item_B['follower_count']
    
    # If user's choice is A
    if choice == 'A':
        if followers_A > followers_B:
            # Clear the console and update score
            clear()
            print(logo)
            score += 1
            print(f'\nYou got it! Current score: {score}.')
            # Keep item A and randomize item B for next comparison
            item_A = item_A
            item_B = random.choice(data)
            return score, item_A, item_B, end_game
        else:
            # Clear the console and end the game
            clear()
            print(logo)
            print(f'\nWrong. You lose! \n\nFinal score: {score}.')
            end_game = True
            
    # If user's choice is B
    elif choice == 'B':
        if followers_B > followers_A:
            # Clear the console and update score
            clear()
            print(logo)
            score += 1
            # Keep item B as item A for next comparison, and randomize item B
            print(f'\nYou got it! Current score: {score}.')
            item_A = item_B
            item_B = random.choice(data)
            return score, item_A, item_B, end_game
        else:
            # Clear the console and end the game
            clear()
            print(logo)
            print(f'\nWrong. You lose! \n\nFinal score: {score}.')
            end_game = True
    return score, item_A, item_B, end_game

# Randomize two initial items    
item_A = random.choice(data)
item_B = random.choice(data)

score = 0
end_game = False

# Loop until game ends
while not end_game:
    # Make sure item_A and item_B are not the same
    while item_A == item_B:
        item_B = random.choice(data)
    
    # Print the two items and ask user for choice            
    print(f"\nA: {item_A['name']}, a {item_A['description']}, from {item_A['country']}.")
    print(vs)
    print(f"\nB: {item_B['name']}, a {item_B['description']}, from {item_B['country']}.")
    choice = input("\nWho has more followers? Type 'A' or 'B': ").upper()
    
    # Compare the two items and update score and game status
    score, item_A, item_B, end_game = compare_items(choice, item_A, item_B, score, end_game)