import random
import os # For the clear function

logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # 'cls' for Windows / 'clear' for Unix-based systems

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def deal_card():
    return random.choice(cards)

keep_playing = True

while keep_playing:
    play_blackjack = input("Do you want to play a game of Blackjack. Type 'y' or 'n': ").lower()
    if play_blackjack == 'n':
        keep_playing = False
    clear()
    print(logo)
    player_cards = [deal_card(), deal_card()] # Adds two cards to the player's hand
    player_score = sum(player_cards) # Current score
    dealer_cards = [deal_card()] # Adds one card to the dealer's had
    
    next_card = True
    
    while next_card and player_score < 21:
        print(f'Your cards: {player_cards}. Current score: {player_score}.')
        print(f"Computer's first card: {dealer_cards}")
        another_card = input("Type 'y' to get another card. Type 'n' to pass: ").lower()
        if another_card == 'n':
            next_card = False
            break
        player_cards += [deal_card()]
        player_score = sum(player_cards)
        if 11 in player_cards and player_score > 21:
            player_score -= 10
    
    dealer_score = sum(dealer_cards) # Current dealer score
    
    while dealer_score < 17:
        dealer_cards += [deal_card()] # Dealer draws cards until a score of > 16 OR > players_score
        dealer_score = sum(dealer_cards)
        if 11 in dealer_cards and dealer_score > 21:
            dealer_score -= 10
    
    print(f'Your final hand: {player_cards}. Final score: {player_score}.')
    print(f"Dealer's final hand: {dealer_cards}. Final score: {dealer_score}.")
    
    if player_score > 21:
        print('You went over. You lose!')
    elif dealer_score > 21:
        print('Dealer went over. You win!')        
    elif player_score == dealer_score:
        print('Draw!')        
    elif player_score > dealer_score:
        print('You win!')
    elif player_score < dealer_score:
        print('You lose!')