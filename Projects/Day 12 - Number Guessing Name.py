import random

logo = r'''____  ____  ____  ____  ____  _________  ____  ____  ____  _________  ____  ____  ____  ____  ____  ____ 
||G ||||U ||||E ||||S ||||S ||||       ||||T ||||H ||||E ||||       ||||N ||||U ||||M ||||B ||||E ||||R ||
||__||||__||||__||||__||||__||||_______||||__||||__||||__||||_______||||__||||__||||__||||__||||__||||__||
|/__\||/__\||/__\||/__\||/__\||/_______\||/__\||/__\||/__\||/_______\||/__\||/__\||/__\||/__\||/__\||/__\|
'''

print(logo)
print('Welcome to the Number Guessing Game!')

EASY_LEVEL_ATTEMPTS = 10
HARD_LEVEL_ATTEMPTS = 5

def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ")
    if level == 'easy':
        return EASY_LEVEL_ATTEMPTS
    else:
        return HARD_LEVEL_ATTEMPTS

attempts = set_difficulty()
print("I'm thinking of a number between 1 and 100.")
answer = random.randint(1, 100) # Randomizes a number between 1 and 100

guess = 0
end_game = False # Flag for ending the game

def check_answer(guess, answer, attempts):
    '''Checks answer against guess. Returns the number of attempts remaining.'''
    if guess > answer:
        print('Too high.')
        return attempts - 1
    if guess < answer:
        print('Too low.')
        return attempts - 1
    else:
        print(f'You got it! The answer was {answer}.')
        global end_game # end_game is a global variable
        end_game = True

while not end_game:
    print(f'You have {attempts} attempts remaining to guess the number.')
    guess = int(input('Make a guess: '))
    attempts = check_answer(guess, answer, attempts)
    if attempts == 0:
        print('You have run out of guesses. You lose.')
        end_game = True
    elif guess != answer:
        print('Guess again.')