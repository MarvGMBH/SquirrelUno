from __future__ import annotations
from utils import UIDObj
from card_logic import CardType, CardColor, Card, NumberCard, JokerCard, Stack

class Player(UIDObj):
    def __init__(self, name:str, game_position:int):
        super().__init__()
        self.name = name
        self.game_position = game_position
        self.hands = Stack(self.uid, {})
    
    @classmethod
    def get_uid(cls, name:str):
        player_uid = None
        
        for uid, player_obj in UIDObj.iterate(Player):
            if player_obj.name != name:
                continue
            player_uid = uid
        
        if player_uid is None:
            raise ValueError(f"No match for Player:{name}...")
        
        return player_uid
    
    def card_count(self):
        return len(self.hands.cards)

class GameMaster(UIDObj):
    def __init__(self, players:list):
        super().__init__()
        
        self.players = self.init_players(players)
        self.player_turn = Player.get_uid(players[0])
        
        self.global_stack = Stack("global", self.create_cards())
        self.game_direction = -1
        self.game_active = True
        
    def create_cards(self):
        cards = {}
        
        for color in CardColor:
            for number in range(1, 9):
                new_card = NumberCard(number, color.value)
    
    def init_players(self, players:list):
        created_players = {}
        
        for index, player_name in enumerate(players):
            new_player = Player(player_name, index)
            created_players[new_player.uid] = new_player
        
        return created_players

    def get_players_for_cycle(self):
        current_player = self.players[self.player_turn]
        
        next_player_pos = current_player.game_position + self.game_direction
        if next_player_pos < 0:
            next_player_pos = len(self.players)-1
        elif next_player_pos > len(self.players)-1:
            next_player_pos = 0
        
        for uid, player_obj in UIDObj.iterate(Player):
            if player_obj.game_position == next_player_pos:
                next_player = player_obj
        
        return current_player, next_player 

    def show_current_player_deck(self, player:Player):
        others_hands = ""
        for _, other in UIDObj.iterate(Player):
            if other.uid == player.uid:
                continue
            others_hands += f"{other.name} {other.card_count()}\n"
            
        print("=========================",
              f"player turn: {player.name}",
              f"other players decks:\n{others_hands}",
              f"\ron your hands:\n{player.hands}",
              sep="\n")
    
    def game_cycle(self):
        current_player, next_player = self.get_players_for_cycle()
        self.show_current_player_deck(current_player)
        self.player_turn = next_player.uid
        input()
    
    def start(self):
        while self.game_active:
            self.game_cycle()