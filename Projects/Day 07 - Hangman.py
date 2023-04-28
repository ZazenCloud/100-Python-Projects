import random
import os # For the clear function
# Download hangman_art.py and hangman_words.py (located on this repository) and move them to same folder of this file
import hangman_art
import hangman_words

def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # 'cls' for Windows / 'clear' for Unix-based systems

chosen_word = random.choice(hangman_words.word_list) # Choose one animal randomly from the list
word_length = len(chosen_word)
end_of_game = False
lives = 6
hint_two = 0
error_list = []

print(hangman_art.logo)

# Creates an underscore for each letter
display = []
for _ in range(word_length):
    display += "_"

while not end_of_game: # Runs until winning or losing condition
    guess = input("\nGuess a letter: ").lower()
    clear() # Clears the console/terminal

    # Check if player repeats a guess
    if guess in display or guess in error_list:
        print('\nYou already guessed that word!')

    # Check if guess appears in the word
    for position in range(word_length):
        letter = chosen_word[position]
        if letter == guess:
            display[position] = guess

    # Check if guess is wrong
    if guess not in chosen_word and guess not in error_list: # Check repetitions
        lives -= 1    
        error_list += guess
        if lives > 1:
            print(f"\nOops, {guess} is not in the word. Death is closer...")
            if lives == 4: # Hint 1 after losing 2 lives
                print("\nHint: it's an animal!") 
            if lives == 2 and hint_two == 0: # Hint 2 after losing 4 lives
                print(f'\nHint: it starts with {chosen_word[0]} and ends with {chosen_word[word_length - 1]}.') # Reveals first and last letters
                hint_two += 1
        if lives == 0:
            end_of_game = True
            print(f'\nThe word was {chosen_word}...')
            print(hangman_art.skull)
    
    # Check if user got all letters right
    if "_" not in display:
        end_of_game = True
        print(f"\n{' '.join(display)}") # Join all the elements in the list and turn it into a String
        print(hangman_art.trophy)
        
    # Art for each life
    if end_of_game == False and lives > 0:
        print(hangman_art.stages[lives])
        print(f"{' '.join(display)}")
