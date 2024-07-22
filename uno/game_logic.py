from __future__ import annotations
from card_logic import CardType, CardColor, Card, NumberCard, JokerCard, Stack
from utils import UIDObj
import random
import os

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
        self.draw_stack = Stack("draw", {})
        self.game_stack = Stack("game", {})
        
        print("lay down first card...")
        self.lay_down_first_card()
        print("give player cards...")
        self.give_players_cards()
        print("fill draw stack...")
        self.fill_draw_stack()
        
        self.game_direction = -1
        self.game_active = True
        
    def lay_down_first_card(self):
        while True:
            random_card_uid = random.choice(list(self.global_stack.cards))
            random_card_obj = UIDObj.get(random_card_uid)
            
            if random_card_obj.card_type == CardType.joker:
                continue
            
            random_card_obj.transfer_owner("global", "game")
            break
            
    def give_players_cards(self):
        for player in self.players.values():
            for i in range(7):
                random_card_uid = random.choice(list(self.global_stack.cards))
                random_card_obj = UIDObj.get(random_card_uid)
                random_card_obj.transfer_owner("global", player.uid)
    
    def fill_draw_stack(self):
        cards_tuple = tuple(self.global_stack.cards.values())
        
        for card in cards_tuple:
            card.transfer_owner("global", "draw")
    
    def create_cards(self):
        cards = {}
        
        for color in CardColor:
            if color == CardColor.no_color:
                continue
            
            for number in range(1, 10):
                new_card = NumberCard(number, color)
                new_card.owner = "global"
                cards[new_card.uid] = new_card
                
            draw_2 = JokerCard(color, "draw 2")
            draw_2.owner = "global"
            cards[draw_2.uid] = draw_2
            draw_4 = JokerCard(color, "draw 4")
            draw_4.owner = "global"
            cards[draw_4.uid] = draw_4
            draw_4_no_color = JokerCard(CardColor.no_color, "draw 4")
            draw_4_no_color.owner = "global"
            cards[draw_4_no_color.uid] = draw_4_no_color

        return cards
    
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

    def show_censor_part(self, player:Player):
        os.system("clear")
        print("#########################################")
        print("#########################################")
        print(f" next player please: {player.name}")
        print("#########################################")
        print("#########################################")
        input("press enter to continue")
        os.system("clear")

    def show_current_player_deck(self, player:Player):
        os.system("clear")
        others_hands = ""
        for _, other in UIDObj.iterate(Player):
            if other.uid == player.uid:
                continue
            others_hands += f"{other.name} {other.card_count()}\n"
            
        print("=========================",
              f"player turn: {player.name}",
              f"top card: {self.game_stack.last_added_card}",
              f"other players decks:\n{others_hands}",
              f"\ron your hands:\n{player.hands}",
              sep="\n")
        return input("make your move: ")
    
    def game_cycle(self):
        current_player, next_player = self.get_players_for_cycle()
        self.show_current_player_deck(current_player)
        self.player_turn = next_player.uid
        self.show_censor_part(next_player)
    
    def start(self):
        print(self.global_stack)
        print("draw")
        print(self.draw_stack)
        for player in self.players.values():
            print(player.name)
            print(player.hands)
        
        input()
        while self.game_active:
            self.game_cycle()