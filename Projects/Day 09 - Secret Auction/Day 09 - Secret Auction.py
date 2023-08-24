import os

logo = r'''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\
                       .-------------.
                      /_______________\
'''


def clear():
    # 'cls' for Windows / 'clear' for Unix-based systems
    os.system('cls' if os.name == 'nt' else 'clear')


print(logo)
print("Welcome to the Secret Auction!")
auction_end = False
# Key: name / Value: bid
bids = {}
while not auction_end:
    name = input('What is your name?\n')
    price = int(input('What is your bid?\n$'))
    # Add `name: value` pair to the dictionary
    bids[name] = price
    another_bidder = input("Are there any other bidders? Type 'yes' or 'no'\n")
    if another_bidder == 'no':
        # Ends loop
        auction_end = True
    clear()

# Loops through the dictionary
for bidder in bids:
    highest_bid = 0
    # If value is higher than previous iterations
    if bids[bidder] > highest_bid:
        # Current value is passed to the variable `highest_bid`
        highest_bid = bids[bidder]
        # Current key is passed to the variable `winner`
        winner = bidder

print(f'The winner is {winner} with a bid of ${highest_bid}')
