from __future__ import annotations
from utils import UIDObj
from enum import Enum

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
    
    def transfer_owner(self, owner_uid:str, other_uid:str):
        if self.owner is None:
            raise ValueError(f"card canot be transfered to {other_uid} cause no prev owner")
        if self.owner != owner_uid:
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
    
    def make_action(self):
        print(f"action from joker card {self.uid}")
    
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
        self.cards = cards
        self.owner = owner
        
        self.last_added_card = None
    
    def add_card(self, card_obj:Card):
        self.cards[card_obj.uid] = card_obj
        self.last_added_card = card_obj
    
    def remove_card(self, card_obj:Card):
        self.cards.pop(card_obj.uid, None)
    
    def __str__(self):
        output = ""
        sorted_cards = sorted(self.cards.items(), key=lambda item: item[1].color.value)
        for uid, card in sorted_cards:
            output += f"{card}\n"
        return output
    