from game_logic import GameMaster, Stack, NumberCard, JokerCard, CardColor
import random

def main(debug_active:bool):
    players = []
    
    for i in range(1, 6):
        name = input(f"Player {i}/5 or 'go' to start: ")
        if name == "go":
            break
        players.append(name)
        
    game = GameMaster(players)
    game.start()
    
if __name__ == "__main__":
    main()
