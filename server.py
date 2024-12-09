import socket
import random

# Define constants for card values
CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Function to calculate the value of a hand
def calculate_hand_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    # Adjust for Aces
    num_aces = hand.count('A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

# Function to deal cards
def deal_cards():
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
             '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
             '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
             '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',]
    random.shuffle(cards)
    return [cards.pop(), cards.pop()]

# Function to play a hand
def play_hand(connection):   
    player_hand = deal_cards()
    dealer_hand = deal_cards()

    player_bet = int(connection.recv(1024).decode())
    if player_bet < 10:
        player_bet = 10
        print(f"You bet has been increased to $10 as that is the minimum")

    connection.send(f"Player's hand: {player_hand}\n".encode())
    connection.send(f"Dealer's upcard: {dealer_hand[0]}\n".encode())
    
    # Implement the game logic here (hit, stand, double down)
    while True:
        connection.send("\nOptions:\n1) Hit\n2) Stand\n3) Double down\nEnter your choice: ".encode())
        choice = connection.recv(1024).decode()

        if choice == '1':
            player_hand.append(deal_cards()[0])
            connection.send(f"Player's hand: {player_hand}\n".encode())
            if calculate_hand_value(player_hand) > 21:
                connection.send("Bust! You lose.".encode())
                break
        elif choice == '2':
            break
        elif choice == '3':
            player_bet *= 2
            player_hand.append(deal_cards()[0])
            connection.send(f"Player's hand: {player_hand}\n".encode())
            break
        else:
            connection.send("Invalid choice. Please try again.".encode())

    # Dealer's turn
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_cards()[0])

    connection.send(f"\nPlayer's hand: {player_hand}\nDealer's hand: {dealer_hand}\n".encode())

    # Determine the winner
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value > 21:
        connection.send("Bust! You lose.".encode())        
    elif dealer_value > 21:
        connection.send(f"Dealer busts! You win ${player_bet}.".encode())
    elif player_value > dealer_value:
        connection.send(f"You win ${player_bet}.".encode())
    elif player_value < dealer_value:
        connection.send("Dealer wins. You lose.".encode())
    else:
        connection.send("It's a tie. Your bet is returned.".encode())
    

# Function to start the server
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    finish = True
    
    print(f"Server listening on port {port}...")

    while finish == True:
        connection, address = server_socket.accept()
        print(f"Player connected from {address}")

        connection.send("Welcome to Blackjack!\n".encode())

        while True:
            connection.send("\nOptions:\n1) Play a hand\n2) Exit\nEnter your choice: ".encode())
            choice = connection.recv(1024).decode()

            if choice == '1':
                connection.send("Enter your bet (minimum $10): ".encode())
                play_hand(connection)
            elif choice == '2':
                connection.send("Goodbye!".encode())
                connection.close()
                finish = False
                break
            else:
                connection.send("Invalid choice. Please try again.".encode())

    server_socket.close()
if __name__ == "__main__":
    # Specify the port number for the server
    port_number = 12345
    start_server(port_number)