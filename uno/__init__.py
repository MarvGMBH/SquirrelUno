from game_logic import GameMaster, Stack, NumberCard, JokerCard, CardColor
import os
import time

# ANSI escape codes for colors
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_BLUE = "\033[38;5;45m"
LIGHT_PINK = "\033[38;5;218m"
WHITE = "\033[38;5;15m"
RED = "\033[31m"
MAGENTA = "\033[35m"
ORANGE = "\033[38;5;208m"
CYAN = "\033[36m"
LIGHT_RED = "\033[91m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

# Function to clear the terminal screen
def clear_screen():
    os.system('clear')

# Function to display the UNO game logo
def display_logo():
    uno_logo = """
    __    __  __  __    __ 
    / / /\\ \\ || || || /\\ \\ \\
    |  \\//  \\|| || |||  \\//  \\
    | | \\  / || || ||| | \\  / |
    | |  \\/  || || ||| |  \\/  |
    \\_\\_/\\_/ |_||_| \\_\\_/\\_/ 
    """
    print(f"{RED}{uno_logo}{RESET}")
    input(f"{MAGENTA}Press Enter to continue...{RESET}")

# Function to display a message from the creator
def display_creator_message():
    creator_message = (f"{ORANGE}#############################################################{RESET}\n"
                       f"{' '*61}\n"
                       f"{' '*61}\n"
                       f"{' '*10}{LIGHT_BLUE}{BOLD}G{RESET}{LIGHT_PINK}{BOLD}a{RESET}{WHITE}{BOLD}m{RESET}{LIGHT_PINK}{BOLD}e {RESET}{LIGHT_BLUE}{BOLD}m{RESET}{LIGHT_PINK}{BOLD}a{RESET}{WHITE}{BOLD}d{RESET}{LIGHT_PINK}{BOLD}e {RESET}{LIGHT_BLUE}{BOLD}b{RESET}{LIGHT_PINK}{BOLD}y {RESET}{WHITE}{BOLD}C{RESET}{LIGHT_PINK}{BOLD}h{RESET}{LIGHT_PINK}{BOLD}i{RESET}{LIGHT_BLUE}{BOLD}p{RESET}{LIGHT_PINK}{BOLD}p{RESET}{WHITE}{BOLD}e{RESET}{LIGHT_PINK}{BOLD}r{RESET}{LIGHT_BLUE}{BOLD}f{RESET}{LIGHT_PINK}{BOLD}l{RESET}{WHITE}{BOLD}u{RESET}{LIGHT_PINK}{BOLD}f{RESET}{LIGHT_BLUE}{BOLD}f :P{RESET}\n"
                       f"{' '*61}\n"
                       f"{' '*61}\n"
                       f"{ORANGE}#############################################################{RESET}\n")
    print(creator_message)
    input(f"{MAGENTA}Press Enter to continue...{RESET}")

# Function to ask for player names
def ask_players():
    players = []
    while len(players) < 2:
        clear_screen()
        for i in range(1, 6):
            name = input(f"{CYAN}Enter Player {i} name or type {LIGHT_RED}'go'{CYAN} to start the game: {RESET}")
            if name.lower() == "go" and len(players) >= 2:
                return players
            if name.lower() == "go":
                print(f"{RED}At least two players are required to start the game!{RESET}")
                time.sleep(2)
                break
            players.append(name)
        else:
            if len(players) >= 2:
                return players
            print(f"{RED}At least two players are required to start the game!{RESET}")
            players = []
            time.sleep(2)

# Function to display a detailed tutorial for the UNO game
def tutorial():
    pages = [
        (f"{ORANGE}#############################################################{RESET}\n"
         f"{LIGHT_BLUE}UNO Game Tutorial - Page 1{RESET}\n"
         f"{ORANGE}#############################################################{RESET}\n\n"
         f"{CYAN}Types of Cards{RESET}\n"
         f"{GREEN}- Number Cards: Each card has a number and a color.{RESET}\n"
         f"{YELLOW}- Reverse Cards: Reverses the direction of play.{RESET}\n"
         f"{RED}- Draw 4 Cards: The next player draws four cards.{RESET}\n"
         f"{GREEN}- Draw 2 Cards: The next player draws two cards.{RESET}\n"
         f"{LIGHT_BLUE}- Wild Cards: Can be played at any time and allows the player to choose the color.{RESET}\n"
         f"{MAGENTA}Press Enter to continue...{RESET}\n"),
        (f"{ORANGE}#############################################################{RESET}\n"
         f"{LIGHT_BLUE}UNO Game Tutorial - Page 2{RESET}\n"
         f"{ORANGE}#############################################################{RESET}\n\n"
         f"{CYAN}How to Play{RESET}\n"
         f"{GREEN}1. When it's your turn, type the number corresponding to the card you want to play.{RESET}\n"
         f"{YELLOW}2. If you can't play any card, type {RED}'draw'{YELLOW} to take a new card.{RESET}\n"
         f"{RED}3. After drawing, you can try to play a card if possible or type {LIGHT_BLUE}'next'{RED} to end your turn.{RESET}\n"
         f"{GREEN}4. Repeat the steps until a player has no cards left and wins the game!{RESET}\n"
         f"{MAGENTA}Press Enter to continue...{RESET}\n"),
        (f"{ORANGE}#############################################################{RESET}\n"
         f"{LIGHT_BLUE}UNO Game Tutorial - Page 3{RESET}\n"
         f"{ORANGE}#############################################################{RESET}\n\n"
         f"{CYAN}Game Strategies{RESET}\n"
         f"{GREEN}- Keep track of the cards that have been played.{RESET}\n"
         f"{YELLOW}- Try to save Wild and Draw cards for strategic moments.{RESET}\n"
         f"{RED}- Pay attention to the colors other players have, and try to change the color if it benefits you.{RESET}\n"
         f"{GREEN}- Use Reverse and Skip cards to your advantage to disrupt other players' turns.{RESET}\n"
         f"{MAGENTA}Press Enter to continue...{RESET}\n"),
        (f"{ORANGE}#############################################################{RESET}\n"
         f"{LIGHT_BLUE}UNO Game Tutorial - Page 4{RESET}\n"
         f"{ORANGE}#############################################################{RESET}\n\n"
         f"{CYAN}Endgame Tips{RESET}\n"
         f"{GREEN}- When you have one card left, remember to shout 'UNO!' or you may have to draw more cards.{RESET}\n"
         f"{YELLOW}- Try to play high-value cards early to avoid being stuck with them at the end.{RESET}\n"
         f"{RED}- Plan ahead for the last few turns, thinking about the cards you have and the potential plays from opponents.{RESET}\n"
         f"{GREEN}- Keep an eye on your opponents' card counts and play defensively if necessary.{RESET}\n"
         f"{MAGENTA}Press Enter to start the game...{RESET}\n")
    ]
    for page in pages:
        clear_screen()
        print(page)
        input()

# Function to display a hidden pride flag message
def display_pride_message():
    pride_message = (f"{RED}P{RESET}{ORANGE}r{RESET}{YELLOW}i{RESET}{GREEN}d{RESET}{LIGHT_BLUE}e{RESET}{MAGENTA} :){RESET}")
    print(pride_message)

# Main function to start the UNO game
def main(debug_active: bool):
    clear_screen()
    display_logo()
    clear_screen()
    display_creator_message()
    players = ask_players()
    tutorial()
    
    clear_screen()
    display_pride_message()  # Display hidden pride flag message
    print(f"{YELLOW}Preparing the game with {len(players)} players...{RESET}")
    game = GameMaster(players)
    print(f"{GREEN}Game setup complete!{RESET}")
    input(f"{MAGENTA}Press Enter to start the game...{RESET}")

    game.start()

if __name__ == "__main__":
    main(debug_active=False)
