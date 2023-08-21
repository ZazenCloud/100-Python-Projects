import os

# Morse Code dictionary
morse_dict = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", "0": "-----", " ": "/",
}

# Reverse Morse Code dictionary
reverse_morse_dict = {value: key for key, value in morse_dict.items()}

# Flag to control the running state of the program
running = True


# Function to clear the console screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


while running:
    clear()
    # User prompt for selecting the operation (encode or decode)
    option = input(
        "Morse Encoder/Decoder\n\n"
        "Enter 1 for encoding.\nEnter 2 for decoding.\nEnter 0 to exit.\n\n"
    )
    output = ""
    if option == "1":
        valid = False
        while not valid:
            clear()
            # User input for the phrase to be encoded
            phrase = input("Insert your phrase to be encoded:\n")
            try:
                # Encode each character of the phrase into Morse Code
                for char in phrase:
                    output += morse_dict[char.upper()] + " "
                print(f"\n{output}")
                valid = True
                # Ask user if they want to encode/decode again or exit
                again = input(
                    "\nAgain?\nEnter Y to encode/decode again "
                    "or anything else to exit.\n\n"
                )
                if again.upper() != "Y":
                    running = False
            except KeyError:
                print(
                    "Invalid character. Please use only alphanumeric "
                    "(A-Z / 0-9) characters and spaces."
                )
                input("Press Enter to continue.\n")
    elif option == "2":
        valid = False
        while not valid:
            clear()
            # User input for the phrase to be encoded
            code = input("Insert your code to be decoded:\n")
            try:
                # Decode each Morse Code segment back into a character
                for char in code.split(" "):
                    output += reverse_morse_dict[char]
                print(f"\n{output}")
                valid = True
                # Ask user if they want to encode/decode again or exit
                again = input(
                    "\nAgain?\nEnter Y to encode/decode "
                    "again or anything else to exit.\n\n"
                )
                if again.upper() != "Y":
                    running = False
            except KeyError:
                print(
                    "Error. Make sure you typed a valid morse code.\nOnly . "
                    "(dots), - (hyphens), / (forward slashes) and "
                    "spaces are allowed."
                )
                input("Press Enter to continue.\n")
    elif option == "0":
        running = False
    else:
        pass
