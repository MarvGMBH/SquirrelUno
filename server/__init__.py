from game_logic import GameMaster, Stack, NumberCard, JokerCard, CardColor
from threading import Thread

def main():
    players = []
    while True:
        if len(players) > 5:
            break
                
        name = input("Create Player: ")
        if name == "#del":
            del_name = players.pop(-1)
            print(f"{del_name} deleted")
        elif name == "go":
            break
        else:
            players.append(name)
    
    game = GameMaster(players)
    game_thread = Thread(target=game.start)
    game_thread.start()
    game.start_server()

if __name__ == "__main__":
    main()
