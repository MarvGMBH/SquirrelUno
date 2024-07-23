from __future__ import annotations
from utils import UIDObject, ComponentManager
from collections import OrderedDict
from enum import Enum
import random

try:
    from game_logic import Player
except ImportError:
    pass

class CardType(Enum):
    NUMBER = "number"
    JOKER = "joker"

class CardColor(Enum):
    NO_COLOR = "no_color"
    RED = "red"
    GRENN = "green"
    BLUE = "blue"
    YELLOW = "yellow"

class Card(UIDObject):
    def __init__(self, card_type:CardType):
        super().__init__()
        self.card_type = card_type
        self.owner = None
        self._new_card = False

    def get_stack_based_on_owner(self, owner_uid:str):
        for uid, stack_obj in ComponentManager.iterate_uid_objects(Stack):
            if stack_obj.owner == owner_uid:
                return stack_obj
        raise ValueError(f"No stack found for owner UID: {owner_uid}")

    def transfer_owner(self, owner_uid:str, other_uid:str, *, forced=False, new_card=False):
        if self.owner is None:
            raise ValueError(f"Card cannot be transferred to {other_uid} because it has no previous owner")
        if self.owner != owner_uid and not forced:
            raise ValueError(f"Card {self.uid} does not belong to {owner_uid}")

        owner_stack = self.get_stack_based_on_owner(owner_uid)
        other_stack = self.get_stack_based_on_owner(other_uid)

        owner_stack.remove_card(self)
        other_stack.add_card(self, new_card)
        self.owner = other_uid
    
    def set_new_card(self):
        self._new_card = True
    
    def clear_new_flag(self):
        self._new_card = False

    def __str__(self):
        new_tag = "   "
        if self._new_card:
            new_tag = "NEW "
        return f"{new_tag}{self.card_type} {self.owner}"

class NumberCard(Card):
    def __init__(self, number:int, color:CardColor):
        super().__init__(CardType.NUMBER)
        self.__number = number
        self.__color = color

    @property
    def number(self):
        return self.__number

    @property
    def color(self):
        return self.__color

    def __str__(self):
        new_tag = "   "
        if self._new_card:
            new_tag = "NEW "
        
        color_codes = {
            'red': '\033[31m',
            'blue': '\033[34m',
            'yellow': '\033[33m',
            'green': '\033[32m',
            'reset': '\033[0m'
        }
        
        color_start = color_codes.get(self.color.value, color_codes['reset'])
        color_end = color_codes['reset']

        return f"{new_tag}{color_start}{self.color.value} {self.number}{color_end}"


class JokerCard(Card):
    def __init__(self, color:CardColor, title:str):
        super().__init__(CardType.JOKER)
        self.__color = color
        self.__title = title

    def make_action(self, next_player):
        if self.title.startswith("draw"):
            _, count = self.title.split(" ")
            global_cards = ComponentManager.get_component("draw")

            for _ in range(int(count)):
                random_card_uid = random.choice(list(global_cards.cards))
                random_card_obj = ComponentManager.get_uid_object(random_card_uid)
                random_card_obj.transfer_owner("draw", next_player.uid, forced=True, new_card=True)
                
            return "draw-ok"
        elif self.title == "reverse":
            game_master = ComponentManager.get_component("game_master")
            if len(game_master.players) == 2:
                return "reverse-same-again"
            game_master.game_direction = 1 if game_master.game_direction == -1 else -1
            return "reverse-ok"

    @property
    def color(self):
        return self.__color

    @property
    def title(self):
        return self.__title

    def __str__(self):
        new_tag = "   "
        if self._new_card:
            new_tag = "NEW "
        
        color_codes = {
            'red': '\033[31m',
            'blue': '\033[34m',
            'yellow': '\033[33m',
            'green': '\033[32m',
            'no_color': '\033[38;5;214m',  # Gold/Orange
            'reset': '\033[0m'
        }
        
        color_start = color_codes.get(self.color.value, color_codes['reset'])
        color_end = color_codes['reset']

        if self.color != CardColor.NO_COLOR:
            return f"{new_tag}{color_start}{self.color.value} {self.title}{color_end}"
        else:
            return f"{new_tag}{color_start}{self.title}{color_end}"

class Stack(UIDObject):
    def __init__(self, owner:str, cards:dict[str, Card], sorted_stack=False):
        super().__init__()
        self.sorted_stack = sorted_stack
        card_list = cards.items()
        if sorted_stack:
            card_list = sorted(card_list, key=lambda item: item[1].color.value)
        self.cards = OrderedDict(card_list)
        self.owner = owner
        self.last_added_card = None
        
    def shuffle_deck(self, remain_last_card=False):
        if remain_last_card:
            last_card_uid = self.last_added_card.uid
        
        items = list(self.cards.items())
        random.shuffle(items)
        self.cards = OrderedDict(items)
        
        if remain_last_card:
            last_card = self.cards.pop(last_card_uid)
            self.cards[last_card_uid] = last_card
    
    def clear_new_flag(self):
        for uid, card_obj in self.cards.items():
            card_obj.clear_new_flag()

    def get_card_per_index(self, index:int):
        try:
            return list(self.cards.values())[index]
        except IndexError:
            raise ValueError(f"No card at index: {index}")

    def add_card(self, card_obj:Card, new_flag=False):
        if new_flag:
            card_obj.set_new_card()
        self.cards[card_obj.uid] = card_obj
        self.last_added_card = card_obj
        if self.sorted_stack:
            self.cards = OrderedDict(sorted(self.cards.items(), key=lambda item: item[1].color.value))

    def remove_card(self, card_obj:Card):
        if card_obj.uid in self.cards:
            del self.cards[card_obj.uid]
        else:
            raise ValueError(f"Card with UID {card_obj.uid} not found in stack")

    def __str__(self):
        return "\n".join(f"{index + 1}: {card}" for index, card in enumerate(self.cards.values()))
