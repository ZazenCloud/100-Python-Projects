import pandas
data = pandas.read_csv("nato_phonetic_alphabet.csv")

# Create a dictionary mapping each letter to its corresponding NATO code
nato_dictionary = {row.letter: row.code for index, row in data.iterrows()}

# Convert each letter of the word to its corresponding NATO phonetic code
word = input("Enter a word: ").upper()
phonetic_word = [nato_dictionary[letter] for letter in word]
print(phonetic_word)
