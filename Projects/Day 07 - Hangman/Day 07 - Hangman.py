import random
import os
import hangman_art
import hangman_words


def clear():
    # 'cls' for Windows / 'clear' for Unix-based systems
    os.system('cls' if os.name == 'nt' else 'clear')


end_of_game = False
lives = 6
hint_two = 0
error_list = []

# Choose one animal randomly from the list
chosen_word = random.choice(hangman_words.word_list)

word_length = len(chosen_word)

# Art
print(hangman_art.logo)

# Creates an underscore for each letter
display = []
for _ in range(word_length):
    display += "_"

# Runs until winning or losing condition
while not end_of_game:
    guess = input("\nGuess a letter: ").lower()
    # Clears the console/terminal
    clear()

    # Check if player repeats a guess
    if guess in display or guess in error_list:
        print('\nYou already guessed that word!')

    # Check if guess appears in the word
    for position in range(word_length):
        letter = chosen_word[position]
        if letter == guess:
            display[position] = guess

    # Check if guess is wrong + repetitions
    if guess not in chosen_word and guess not in error_list:
        lives -= 1
        error_list += guess
        if lives > 1:
            print(f"\nOops, {guess} is not in the word. Death is closer...")
            if lives == 4:
                # Hint 1 after losing 2 lives
                print("\nHint: it's an animal!")
            if lives == 2 and hint_two == 0:
                # Hint 2 after losing 4 lives
                print(f'\nHint: it starts with {chosen_word[0]} and ends with {chosen_word[word_length - 1]}.') # Reveals first and last letters
                hint_two += 1
        if lives == 0:
            end_of_game = True
            print(f'\nThe word was {chosen_word}...')
            print(hangman_art.skull)

    # Check if user got all letters right
    if "_" not in display:
        end_of_game = True
        # Join all the elements in the list and turn it into a String
        print(f"\n{' '.join(display)}")
        print(hangman_art.trophy)

    # Art for each life
    if end_of_game is False and lives > 0:
        print(hangman_art.stages[lives])
        print(f"{' '.join(display)}")
