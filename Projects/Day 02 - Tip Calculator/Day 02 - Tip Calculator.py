print('Welcome to the Tip Calculator.')
bill = float(input('What was the total bill? $'))
tip_percentage = float(input(
    'What percentage tip would you like to give? 10, 12, or 15? '
))
people_number = int(input('How many people to split the bill? '))

tip = bill * (tip_percentage / 100)
bill_plus_tip = bill + tip
each_part = bill_plus_tip / people_number

message = f'Each person should pay: ${each_part:.2f}'
print(message)
