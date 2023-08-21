import os # For the clear function

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
    os.system('cls' if os.name == 'nt' else 'clear') # 'cls' for Windows / 'clear' for Unix-based systems

print(logo)
print("Welcome to the Secret Auction!")
auction_end = False
bids = {} # Key: name / Value: bid
while not auction_end:
    name = input('What is your name?\n')
    price = int(input('What is your bid?\n$'))
    bids[name] = price # Add `name: value` pair to the dictionary
    another_bidder = input("Are there any other bidders? Type 'yes' or 'no'\n")
    if another_bidder == 'no':
        auction_end = True # Ends loop
    clear()

for bidder in bids: # Loops through the dictionary
    highest_bid = 0
    if bids[bidder] > highest_bid: # If value is higher than previous iterations
        highest_bid = bids[bidder] # Current value is passed to the variable `highest_bid`
        winner = bidder # Current key is passed to the variable `winner`
        
print(f'The winner is {winner} with a bid of ${highest_bid}')