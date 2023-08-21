import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)

'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)

'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)

'''

player_move = int(input(
    'What do you choose? Type 0 for Rock, 1 for Paper'
    ' or 2 for Scissors.\n'))
computer_move = random.randint(0, 2)

if player_move == 0:
    print(rock)
    if computer_move == 0:
        print(f'Computer chose:\n{rock}Draw!\n')
    elif computer_move == 1:
        print(f'Computer chose:\n{paper}You lose!\n')
    elif computer_move == 2:
        print(f'Computer chose:\n{scissors}You win!\n')
elif player_move == 1:
    print(paper)
    if computer_move == 0:
        print(f'Computer chose:\n{rock}You win!\n')
    elif computer_move == 1:
        print(f'Computer chose:\n{paper}Draw!\n')
    elif computer_move == 2:
        print(f'Computer chose:\n{scissors}You lose!\n')
elif player_move == 2:
    print(scissors)
    if computer_move == 0:
        print(f'Computer chose:\n{rock}You lose!\n')
    elif computer_move == 1:
        print(f'Computer chose:\n{paper}You win!\n')
    elif computer_move == 2:
        print(f'Computer chose:\n{scissors}Draw!\n')
else:
    print('Invalid move!')
