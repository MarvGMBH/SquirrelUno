from __future__ import annotations
from utils import UIDObj
from collections import OrderedDict
from enum import Enum
import random

try:
    from game_logic import Player
except ImportError:
    pass

class CardType(Enum):
    number = "number"
    joker = "joker"
    
class CardColor(Enum):
    no_color = "no_color"
    red = "red"
    green = "green"
    blue = "blue"
    yellow = "yellow"

class Card(UIDObj):
    def __init__(self, card_type:CardType):
        super().__init__()
        self.card_type = card_type
        self.owner = None
    
    def get_stack_based_on_owner(self, owner_uid):
        for uid, stack_obj in UIDObj.iterate(Stack):
            if stack_obj.owner != owner_uid:
                continue
            return stack_obj
        raise ValueError(f"no stack found for {owner_uid}...")
    
    def transfer_owner(self, owner_uid:str, other_uid:str, *, forced=False):
        if self.owner is None:
            raise ValueError(f"card canot be transfered to {other_uid} cause no prev owner")
        if self.owner != owner_uid and not forced:
            raise ValueError(f"card {self.uid} does not belong to {owner_uid}...")
        
        owner_stack = self.get_stack_based_on_owner(owner_uid)
        other_stack = self.get_stack_based_on_owner(other_uid)
        
        owner_stack.remove_card(self)
        other_stack.add_card(self)
        self.owner = other_uid
    
    def __str__(self):
        return f"{self.card_type} {self.owner}"

class NumberCard(Card):
    def __init__(self, number:int, color:CardColor):
        super().__init__(CardType.number)
        self.__number = number
        self.__color = color
    
    @property
    def number(self):
        return self.__number
     
    @property
    def color(self):
        return self.__color

    def __str__(self):
        return f"{self.color.value} {self.number}"
    
class JokerCard(Card):
    def __init__(self, color:CardColor, title:str):
        super().__init__(CardType.joker)
        self.__color = color
        self.__title = title
    
    def make_action(self, next_player):
        if self.title.startswith("draw"):
            _, count = self.title.split(" ")
            global_cards = UIDObj.stacks["draw"]
                
            for i in range(int(count)+1):
                random_card_uid = random.choice(list(global_cards.cards))
                random_card_obj = UIDObj.get(random_card_uid)
                random_card_obj.transfer_owner("game", next_player.uid, forced=True)           
    
    @property
    def color(self):
        return self.__color
    
    @property
    def title(self):
        return self.__title
    
    def __str__(self):
        if self.color == CardColor.no_color:
            return f"{self.title}"
        else:
            return f"{self.color.value} {self.title}"

class Stack(UIDObj):
    def __init__(self, owner:str, cards:dict[str:Card]):
        super().__init__()
        sorted_cards = sorted(cards.items(), key=lambda item: item[1].color.value)
        self.cards = OrderedDict(sorted_cards)
        self.owner = owner
        
        self.last_added_card = None
    
    def get_card_per_index(self, index:int):
        for i, card_obj in enumerate(self.cards.values()):
            if i != index:
                continue
            return card_obj
    
    def add_card(self, card_obj:Card):
        self.cards[card_obj.uid] = card_obj
        self.last_added_card = card_obj
        sorted_cards = sorted(self.cards.items(), key=lambda item: item[1].color.value)
        self.cards = OrderedDict(sorted_cards)
    
    def remove_card(self, card_obj:Card):
        self.cards.pop(card_obj.uid, None)
    
    def __str__(self):
        output = ""
        for index, (uid, card) in enumerate(self.cards.items()):
            output += f"{index+1}: {card}\n"
        return output
    