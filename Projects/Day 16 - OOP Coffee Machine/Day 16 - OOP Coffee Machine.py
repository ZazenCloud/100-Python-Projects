from oop_cm_resources import Menu, CoffeeMaker, MoneyMachine

# Flag for whether the program should shut down or continue running
shutdown = False

coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()
menu = Menu()

while not shutdown:
    choice = input(f'What would you like? ({menu.get_items()}): ').lower()
    if choice == 'report':
        # Prints the current resources and money
        coffee_maker.report()
        money_machine.report()
    elif choice == 'off':
        # Ends the loop
        shutdown = True
    elif menu.find_drink(choice):
        drink = menu.find_drink(choice)
        # Checks if there are enough resources (water, milk and coffee)
        if coffee_maker.is_resource_sufficient(drink):
            # Asks user for coins and checks if there are enough money
            if money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)
