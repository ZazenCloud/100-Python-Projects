MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

# Initial amounts of resources available
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

water = resources["water"]
milk = resources["milk"]
coffee = resources["coffee"]
money = 0

# Flag for whether the program should shut down or continue running
SHUTDOWN = False


def print_report():
    '''Prints the current amount of water, milk, coffee, and money in the coffee machine.'''
    print(f'Water: {water}ml')
    print(f'Milk: {milk}ml')
    print(f'Coffee: {coffee}ml')
    print(f'Money: ${money}')


def check_resources(choice):
    '''Checks if there are enough resources to make the chosen drink.'''
    if choice == 'espresso':
        if water >= 50 and coffee >= 18:
            return True
        elif water < 50:
            print('Not enough water.')
        else:
            print('Not enough coffee.')
    elif choice == 'latte':
        if water >= 200 and milk >= 150 and coffee >= 24:
            return True
        elif water < 200:
            print('Not enough water.')
        elif milk < 150:
            print('Not enough milk.')
        else:
            print('Not enough coffee.')
    elif choice == 'cappuccino':
        if water >= 250 and milk >= 100 and coffee >= 24:
            return True
        elif water < 250:
            print('Not enough water.')
        elif milk < 100:
            print('Not enough milk.')
        else:
            print('Not enough coffee.')


def check_coins(temp_money, choice):
    '''Checks if the user has inserted enough coins to buy the chosen drink.'''
    change = 0
    if temp_money > 1.5 and choice == "espresso":
        change = temp_money - 1.5
        print(f'Here is ${change} in change.')
        return True, money + 1.5
    elif temp_money == 1.5 and choice == "espresso":
        return True
    elif temp_money > 2.5 and choice == "latte":
        change = temp_money - 2.5
        print(f'Here is ${change} in change.')
        return True
    elif temp_money == 2.5 and choice == "latte":
        return True
    if temp_money > 3.0 and choice == "cappuccino":
        change = temp_money - 3.0
        print(f'Here is ${change} in change.')
        return True
    elif temp_money == 3.0 and choice == "cappuccino":
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")


def update_resources(choice):
    '''Updates the amount of resources and money in the coffee machine after a drink has been made.'''
    if choice == 'espresso':
        return water - 50, milk, coffee - 18, money + 1.5
    if choice == 'latte':
        return water - 200, milk - 150, coffee - 24, money + 2.5
    elif choice == 'cappuccino':
        return water - 250, milk - 100, coffee - 24, money + 3.0


while not SHUTDOWN:
    choice = input('What would you like? (espresso/latte/cappuccino): ').lower()
    if choice == 'report':
        # Prints the current resources and money
        print_report()
    elif choice == 'off':
        # Ends the loop
        SHUTDOWN = True
    elif choice == 'espresso' or choice == 'latte' or choice == 'cappuccino':
        # Checks if there are enough resources (water, milk and coffee)
        if check_resources(choice):
            print('Please insert coins.')
            quarters = int(input('How many quarters? ')) * 0.25
            dimes = int(input('How many dimes? ')) * 0.1
            nickles = int(input('How many nickles? ')) * 0.05
            pennies = int(input('How many pennies? ')) * 0.01
            temp_money = quarters + dimes + nickles + pennies
            # Checks if there are enough money inserted
            if check_coins(temp_money, choice):
                # Updates the resources and deliver the chosen drink
                water, milk, coffee, money = update_resources(choice)
                print(f'Here is your {choice}. Enjoy!')
    else:
        print('Choose a valid option.')
