logo = """           
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88   
            88             88                                 
           ""             88                                 
                          88                                 
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b         88 88       d8 88       88 8PP""""""" 88          
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88          
              88                                             
              88           
"""

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# This function performs the encryption and decryption operations using the Caesar Cipher algorithm
def caesar(text, shift, direction):
  cipher_text = ''
  if direction == 'decode':
      shift *= -1 # Reverse the shift direction if it is decryption
  for letter in text:
    if letter not in alphabet:
      cipher_text += letter # Add non-alphabetic characters directly to the output
    else:
      position = alphabet.index(letter)
      new_position = position + shift
      cipher_text += alphabet[new_position]
    
  if direction == 'encode' or direction == 'decode':
    print(f'The {direction}d text is: {cipher_text}')
  else:
    print('Choose the encode or decode option.')

print(logo)

start_over = ''
first_time = True

# This loop allows the user to repeatedly perform the encryption or decryption operations until they choose to exit
while first_time or start_over == 'yes':
  option = input("\nType 'encode' to encrypt, type 'decode' to decrypt:\n")
  plain_text = input("Type your message:\n").lower()
  shift_amount = int(input("Type the shift number:\n"))
  shift_amount = shift_amount % 26 # Wrap around if the new position is out of range (shift number above 25)
  caesar(text=plain_text, shift=shift_amount, direction=option)
  first_time = False
  start_over = input("\nDo you want to encode/decode another text? Type 'yes' if you do. Type anything else to exit.\n")
