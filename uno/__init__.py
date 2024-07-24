from game_logic import GameMaster, Stack, NumberCard, JokerCard, CardColor, Color
import os
import time

def clear_screen():
    os.system('clear')

def display_logo():
    uno_logo = """
    
    __    __  __  __    __ 
    / / /\\ \\ || || || /\\ \\ \\
    |  \\//  \\|| || |||  \\//  \\
    | | \\  / || || ||| | \\  / |
    | |  \\/  || || ||| |  \\/  |
    \\_\\_/\\_/ |_||_| \\_\\_/\\_/ 
    """
    print(f"{Color.RED}{uno_logo}{Color.RESET}")
    input(f"{Color.MAGENTA}Press Enter to continue...{Color.RESET}")

def display_creator_message():
    creator_message = (f"{Color.ORANGE}#############################################################{Color.RESET}\n"
                       f"{Color.BG_GREEN}{' '*61}{Color.RESET}\n"
                       f"{Color.BG_GREEN}{' '*61}{Color.RESET}\n"
                       f"{Color.BG_GREEN}{' '*20}Game made by Dominik :P{Color.RESET}{Color.BG_GREEN}{' '*20}{Color.RESET}\n"
                       f"{Color.BG_GREEN}{' '*61}{Color.RESET}\n"
                       f"{Color.BG_GREEN}{' '*61}{Color.RESET}\n"
                       f"{Color.ORANGE}#############################################################{Color.RESET}\n")
    print(creator_message)
    input(f"{Color.MAGENTA}Press Enter to continue...{Color.RESET}")

def ask_players():
    players = []
    while len(players) < 2:
        clear_screen()
        for i in range(1, 6):
            name = input(f"{Color.CYAN}Enter Player {i} name or type {Color.LIGHT_RED}'go'{Color.CYAN} to start the game: {Color.RESET}")
            if name.lower() == "go" and len(players) >= 2:
                return players
            if name.lower() == "go":
                print(f"{Color.RED}At least two players are required to start the game!{Color.RESET}")
                time.sleep(2)
                break
            players.append(name)
        else:
            if len(players) >= 2:
                return players
            print(f"{Color.RED}At least two players are required to start the game!{Color.RESET}")
            players = []
            time.sleep(2)

def tutorial():
    pages = [
        (f"{Color.ORANGE}#############################################################{Color.RESET}\n"
         f"{Color.LIGHT_BLUE}UNO Game Tutorial{Color.RESET}\n"
         f"{Color.ORANGE}#############################################################{Color.RESET}\n\n"
         f"{Color.CYAN}Page 1: Types of Cards{Color.RESET}\n"
         f"{Color.LIGHT_GREEN}- Number Cards: Each card has a number and a color.{Color.RESET}\n"
         f"{Color.YELLOW}- Reverse Cards: Reverses the direction of play.{Color.RESET}\n"
         f"{Color.RED}- Draw 4 Cards: The next player draws four cards{Color.RESET}\n"
         f"{Color.GREEN}- Colored Draw 2 Cards: The next player draws two cards{Color.RESET}\n"
         f"{Color.BLUE}- Colored Draw 4 Cards: Similar to Draw 4 but with a specific color.{Color.RESET}\n"
         f"{Color.MAGENTA}Press Enter to continue...{Color.RESET}\n"),
        (f"{Color.ORANGE}#############################################################{Color.RESET}\n"
         f"{Color.LIGHT_BLUE}UNO Game Tutorial{Color.RESET}\n"
         f"{Color.ORANGE}#############################################################{Color.RESET}\n\n"
         f"{Color.CYAN}Page 2: How to Play{Color.RESET}\n"
         f"{Color.LIGHT_GREEN}1. When it's your turn, type the number corresponding to the card you want to play.{Color.RESET}\n"
         f"{Color.YELLOW}2. If you can't play any card, type {Color.RED}'draw'{Color.YELLOW} to take a new card.{Color.RESET}\n"
         f"{Color.RED}3. After drawing, you can try to play a card if possible or type {Color.LIGHT_BLUE}'next'{Color.RED} to end your turn.{Color.RESET}\n"
         f"{Color.GREEN}4. Repeat the steps until a player has no cards left and wins the game!{Color.RESET}\n"
         f"{Color.MAGENTA}Press Enter to start the game...{Color.RESET}\n")
    ]
    for page in pages:
        clear_screen()
        print(page)
        input()

def main(debug_active: bool):
    clear_screen()
    display_logo()
    clear_screen()
    display_creator_message()
    players = ask_players()
    tutorial()
    
    clear_screen()
    print(f"{Color.YELLOW}Preparing the game with {len(players)} players...{Color.RESET}")
    game = GameMaster(players)
    print(f"{Color.GREEN}Game setup complete!{Color.RESET}")
    input(f"{Color.MAGENTA}Press Enter to start the game...{Color.RESET}")

    game.start()
