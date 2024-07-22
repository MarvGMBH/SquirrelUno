from game_logic import GameMaster, Stack, NumberCard, JokerCard, CardColor
import random

def main(debug_active:bool):
    players = ["jack", "marvin", "joe"]
    game = GameMaster(players)
    game.start()
    
if __name__ == "__main__":
    main()
