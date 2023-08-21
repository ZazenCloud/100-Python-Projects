# Read the list of names from the input file
with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()

# Read the contents of the starting letter template
with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter = letter_file.read()
    # Iterate over each name in the list
    for name in names:
        # Remove the newline character from the name
        stripped_name = name.strip("\n")
        # Replace the placeholder with the current name in the letter template
        final_letter = letter.replace("[name]", stripped_name)
        # Create a new file for the personalized letter
        with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.txt", "w") as named_letter:
            # Write the personalized letter to the file
            named_letter.write(final_letter)
