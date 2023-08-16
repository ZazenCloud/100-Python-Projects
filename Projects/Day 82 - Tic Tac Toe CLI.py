import random
import os

tic_tac_graphic = """
|   |   |   |
-------------
|   |   |   |
-------------
|   |   |   |
"""

how_to_play = """
This is a Tic Tac Toe board:

    1   2   3
A |   |   |   |
  -------------
B |   |   |   |
  -------------
C |   |   |   |

Every row is represented by a letter (A, B and C).
And every column is represented by a number (1, 2 and 3).

2 players, represented by X and O, take turns marking the empty boxes.
E.g. B2 for the center box, C3 for the bottom-right box and so on.

A random player is given the X at the start of the game.
The X player makes the first move.

To win the game, one player must have a line with 3 symbols in any direction:

(Horizontal)     (Vertical)       (Diagonal)

| X | X | X |    | X |   |   |    | X |   |   |
-------------    -------------    -------------
|   |   |   |    | X |   |   |    |   | X |   |
-------------    -------------    -------------
|   |   |   |    | X |   |   |    |   |   | X |

"""

signs = ["X", "O"]

available_boxes = [
    "A1", "A2", "A3",
    "B1", "B2", "B3",
    "C1", "C2", "C3"
]

board = [
  ["   ", "   ", "   "],
  ["   ", "   ", "   "],
  ["   ", "   ", "   "]
]

player_moves_list = []
computer_moves_list = []
end_game = False


def mark_board(move, sign):
    """Marks the board with the player's move."""
    row = move[0]
    column = move[1]

    row = row.replace("A", "1")
    row = row.replace("B", "2")
    row = row.replace("C", "3")

    board[int(row) - 1][int(column) - 1] = f" {sign} "


def print_board():
    """Prints the current state of the board."""
    for row in board:
        print("|" + "|".join(row) + "|")
        print("-------------")


def clear():
    """Clears the console screen."""
    # 'cls' for Windows / 'clear' for Unix-based systems
    os.system('cls' if os.name == 'nt' else 'clear')


def check_win(move_list):
    """Checks if a player has won the game."""
    global end_game
    # Set of tuples that represent the winning combinations
    win_combinations = [
        ("A1", "A2", "A3"),
        ("B1", "B2", "B3"),
        ("C1", "C2", "C3"),
        ("A1", "B1", "C1"),
        ("A2", "B2", "C2"),
        ("A3", "B3", "C3"),
        ("A1", "B2", "C3"),
        ("A3", "B2", "C1")
    ]
    # Convert the move list to a set
    move_set = set(move_list)
    # Check if any of the winning combinations is a subset of the move set
    for combination in win_combinations:
        if set(combination).issubset(move_set):
            end_game = True
            return
    # If none of the winning combinations is a subset, return False
    return False

# Start up
clear()
print("Welcome to the Tic Tac Toe CLI!\n")
know = input(
    "Do you know how to play?\n"
    "Enter Y for Yes or anything else for No.\n"
)
if know.upper() != "Y":
    clear()
    print(how_to_play)
    input("Press Enter to start a game.\n")

# Randomly assign player and computer signs
player_sign = signs.pop(random.randint(0, 1))
computer_sign = signs[0]

# If the player is assigned "X", they start the game
if player_sign == "X":
    clear()
    print("You start!\n")
    print(tic_tac_graphic)
    while True:
        player_move = input("\nYour move:\n").upper()
        if player_move not in available_boxes:
            print("Invalid move.\nPlease enter a valid move:")
            print(str(available_boxes))
            continue
        mark_board(player_move, player_sign)
        player_move = available_boxes.pop(available_boxes.index(player_move))
        player_moves_list.append(player_move)
        clear()
        computer_move = random.choice(available_boxes)
        computer_move = available_boxes.pop(available_boxes.index(computer_move))
        computer_moves_list.append(computer_move)
        print(f"Computer played {computer_move}!\n")
        mark_board(computer_move, computer_sign)
        print_board()
        player_move = input("\nYour move:\n").upper()
        if player_move not in available_boxes:
            print("Invalid move.\nPlease enter a valid move:")
            print(str(available_boxes))
            continue
        break
else:
    clear()
    print("Computer started!\n")
    computer_move = random.choice(available_boxes)
    computer_move = available_boxes.pop(available_boxes.index(computer_move))
    computer_moves_list.append(computer_move)
    mark_board(computer_move, computer_sign)
    print_board()
    while True:
        player_move = input("\nYour move:\n").upper()
        if player_move not in available_boxes:
            print("Invalid move.\nPlease enter a valid move:")
            print(str(available_boxes))
            continue
        break

# Main game loop
while not end_game:
    mark_board(player_move, player_sign)
    player_move = available_boxes.pop(available_boxes.index(player_move))
    player_moves_list.append(player_move)
    check_win(player_moves_list)
    clear()
    if end_game:
        winner = "Player"
        break
    elif not available_boxes:
        winner = None
        break
    computer_move = random.choice(available_boxes)
    computer_move = available_boxes.pop(available_boxes.index(computer_move))
    computer_moves_list.append(computer_move)
    mark_board(computer_move, computer_sign)
    check_win(computer_moves_list)
    if end_game:
        winner = "Computer"
        break
    elif not available_boxes:
        winner = None
        break
    print(f"Computer played {computer_move}!\n")
    print_board()
    while True:
        player_move = input("\nYour move:\n").upper()
        if player_move not in available_boxes:
            print("Invalid move.\nPlease enter a valid move:")
            print(str(available_boxes))
            continue
        break

# Game over
print(" GAME  OVER!\n")
print_board()
if winner == "Player":
    print("\nYou won!\n")
elif winner == "Computer":
    print("\nComputer won!\n")
else:
    print("\nDraw!\n")
