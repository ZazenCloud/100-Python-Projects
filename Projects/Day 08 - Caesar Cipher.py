alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

option = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
plain_text = input("Type your message:\n").lower()
shift_amount = int(input("Type the shift number:\n"))

def caesar(text, shift, direction):
  cipher_text = ''
  if direction == 'decode':
      shift *= -1
  for letter in text:
    position = alphabet.index(letter)
    new_position = position + shift
    if new_position > 25:
      new_position = new_position % 26
    elif new_position < 0:
      new_position = new_position % -26
    cipher_text += alphabet[new_position]

  if direction == 'encode' or direction == 'decode':
    print(f'The {direction}d text is {cipher_text}')
  else:
    print('Choose the encode or decode option.')

caesar(text=plain_text, shift=shift_amount, direction=option)
