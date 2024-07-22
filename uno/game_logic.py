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
        UIDObj.stacks["global"] = self.global_stack
        self.draw_stack = Stack("draw", {})
        UIDObj.stacks["draw"] = self.draw_stack
        self.game_stack = Stack("game", {})
        UIDObj.stacks["game"] = self.game_stack
        
        print("lay down first card...")
        self.lay_down_first_card()
        print("give player cards...")
        self.give_players_cards()
        print("fill draw stack...")
        self.fill_draw_stack()
        
        self.game_direction = -1
        self.game_active = True
        self.skip_unlooked = False
        self.last_user_action = None
        
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
        print("\n"*6)
        print(f" next player please: {player.name}")
        print("\n"*6)
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
        return input(f"choose your action\nenter a number from {1} to {len(player.hands.cards)} for the representing card in your deck\nor enter draw to take a card\nwhat should it be {player.name}?\naction: ")
    
    def make_player_action(self, current_player, next_player, action:str, skip_unlooked):
        print("action", action)
        if action == "skip" and skip_unlooked:
            self.last_user_action = "skip"
            return
        elif action == "skip" and not skip_unlooked:
            self.last_user_action = "no-skip"
            return
        
        if action == "draw":
            draw_stack_len = len(self.draw_stack.cards)
            card = self.draw_stack.get_card_per_index(draw_stack_len-1)
            card.transfer_owner("draw", current_player.uid)
            self.last_user_action = "draw"
            return
        
        if action.isdecimal():
            try:
                index = int(action)
            except ValueError:
                self.last_user_action = "invalid-no-int"
                return
            
            game_card = self.game_stack.last_added_card            
            player_card = current_player.hands.get_card_per_index(index-1)
            
            if ((player_card.color == CardColor.no_color or
                  game_card.color == player_card.color) and
                  player_card.card_type == CardType.joker):
                player_card.make_action(next_player)
                
            elif (game_card.card_type == CardType.joker and
                  (game_card.color == CardColor.no_color or
                  game_card.color == player_card.color)):
                pass
            
            elif (game_card.color != player_card.color and
                  game_card.number != player_card.number):
                self.last_user_action = "wrong-card"
                return
                
            print(player_card, "found")
            player_card.transfer_owner(current_player.uid, "game")
            self.last_user_action = "played-card"
            return
        
        self.last_user_action = None
    
    def game_cycle(self):
        current_player, next_player = self.get_players_for_cycle()
        player_action = self.show_current_player_deck(current_player)
        self.make_player_action(current_player, next_player, player_action, self.skip_unlooked)  
        print("last action", self.last_user_action)  
        input("complet cycle")  
        self.player_turn = next_player.uid
        self.show_censor_part(next_player)
    
    def start(self):
        while self.game_active:
            self.skip_unlooked = False
            self.last_user_action = None
            self.game_cycle()
            