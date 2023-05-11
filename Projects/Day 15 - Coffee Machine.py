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
profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

# Flag for whether the program should shut down or continue running
shutdown = False


def print_report():
    '''Prints the current amount of resources and money in the coffee machine.'''
    print(f'Water: {resources["water"]}ml')
    print(f'Milk: {resources["milk"]}ml')
    print(f'Coffee: {resources["coffee"]}ml')
    print(f'Money: ${profit}')


def check_resources(order_ingredients):
    '''Checks if there are enough resources to make the chosen drink.'''
    for item in order_ingredients:
        if order_ingredients[item] >= resources[item]:
            print(f'Sorry there is not enough {item}.')
            return False
        else:
            return True


def check_payment(money_received, drink_cost):
    '''Checks if the user has inserted enough coins to buy the chosen drink.'''
    change = 0
    global profit
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        print(f'Here is ${change} in change.')
        profit += drink_cost
        return True
    elif money_received == drink_cost:
        profit += drink_cost
        return True
    else:
        print("Sorry, that's not enough money. Money refunded.")
        return False


def update_resources(order_ingredients):
    '''Updates the amount of resources in the coffee machine
    after a drink has been made.'''
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]


while not shutdown:
    choice = input('What would you like? (espresso/latte/cappuccino): ').lower()
    if choice == 'report':
        # Prints the current resources and money
        print_report()
    elif choice == 'off':
        # Ends the loop
        shutdown = True
    elif choice == 'espresso' or choice == 'latte' or choice == 'cappuccino':
        drink = MENU[choice]
        # Checks if there are enough resources (water, milk and coffee)
        if check_resources(drink['ingredients']):
            # Asks user for coins
            print('Please insert coins.')
            quarters = int(input('How many quarters? ')) * 0.25
            dimes = int(input('How many dimes? ')) * 0.1
            nickles = int(input('How many nickles? ')) * 0.05
            pennies = int(input('How many pennies? ')) * 0.01
            money_received = quarters + dimes + nickles + pennies
            # Checks if there are enough money inserted
            if check_payment(money_received, drink['cost']):
                # Updates the resources and delivers the chosen drink
                update_resources(drink['ingredients'])
                print(f'Here is your {choice}. Enjoy!')
    else:
        print('Choose a valid option.')
