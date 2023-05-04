import os # For the clear() function

logo = """
 _____________________
|  _________________  |
| |                 | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""

# Clear the console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # 'cls' for Windows / 'clear' for Unix-based systems

# Functions for each arithmetic operation  
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

# Dictionary to store the operations symbols and their corresponding functions
operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

def calculator():
    print(logo)
    num1 = float(input('What is the first number? '))
    for symbol in operations:
        print(symbol)
    operation_symbol = input('Pick an operation from the line above: ')
    num2 = float(input('What is the second number? '))
    answer = operations[operation_symbol](num1, num2) # Calculate the answer using the chosen operation
  
    print(f'{num1} {operation_symbol} {num2} = {answer}')
  
    keep_looping = True # Set a flag to keep looping
  
    while keep_looping:
        cont = input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start over.\n") 
        if cont == 'n': # Loop until the user chooses to start over
            keep_looping = False
            clear()
            calculator() # Recursion
        old_answer = answer
        new_operation_symbol = input('Pick an operation: ')
        new_num = float(input('What is the next number? '))
        answer = operations[new_operation_symbol](answer, new_num)
        print(f'{old_answer} {new_operation_symbol} {new_num} = {answer}')

calculator() # Start the program
