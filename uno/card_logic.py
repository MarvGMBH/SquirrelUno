from __future__ import annotations
from utils import UIDObject, ComponentManager, Color
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
        new_tag = ""
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

    def render(self):
        color_codes = {
            'red': Color.RED,
            'blue': Color.BLUE,
            'yellow': Color.YELLOW,
            'green': Color.GREEN,
            'reset': Color.RESET
        }
        
        color_start = color_codes.get(self.color.value, color_codes['reset'])
        color_end = color_codes['reset']

        return f"{color_start}{self.color.value} {self.number}{color_end}"

    def __str__(self):
        new_tag = ""
        if self._new_card:
            new_tag = f"{Color.LIGHT_GREEN}NEW {Color.RESET}"

        return f"{new_tag}{self.render()}"


class JokerCard(Card):
    def __init__(self, color:CardColor, title:str):
        super().__init__(CardType.JOKER)
        self.__color = color
        self.__title = title

    def make_action(self, last_card, current_player, next_player):
        return f"action {last_card.render()} {current_player.name} vs {next_player.name}", None

    @property
    def color(self):
        return self.__color

    @property
    def title(self):
        return self.__title
    
    def render(self):
        color_codes = {
            'red': Color.RED,
            'blue': Color.BLUE,
            'yellow': Color.YELLOW,
            'green': Color.GREEN,
            'no_color': '\033[38;5;214m',  # Gold/Orange
            'reset': Color.RESET
        }
        
        color_start = color_codes.get(self.color.value, color_codes['reset'])
        color_end = color_codes['reset']

        if self.color != CardColor.NO_COLOR:
            return f"{color_start}{self.color.value} {self.title}{color_end}"
        else:
            return f"{color_start}{self.title}{color_end}"

    def __str__(self):
        new_tag = ""
        if self._new_card:
            new_tag = f"{Color.LIGHT_MAGENTA}NEW {Color.RESET}"
        
        return f"{new_tag}{self.render()}"

class DrawCard(JokerCard):
    def __init__(self, color: CardColor, title: str):
        super().__init__(color, title)
        self.bonus = 0

    def make_action(self, last_card, current_player, next_player):
        game_master = ComponentManager.get_component("game_master")
        
        if last_card.card_type == CardType.JOKER and isinstance(last_card, DrawCard) and self.bonus > 0:
            self.bonus += last_card.bonus
            last_card.bonus = 0
            game_master.newest_draw_card = self
            game_master.draw_card_active = True
            input(f"{self} {self.bonus=} {last_card.bonus=}")
        else:
            _, count = self.title.split(" ")
            count = int(count)
            self.bonus = count
            game_master.newest_draw_card = self
            game_master.draw_card_active = True
            input(f"{self} {self.bonus=}")
            return f"{Color.CYAN}Oh, you laid down a {self} card", f"{current_player.name} laid down a {self}. Lay a similar card or type 'draw' to draw cards."

        return f"{Color.CYAN}Oh no, there's a {self}{Color.CYAN} active{Color.RESET}", None

    def give_out_draw(self, player: Player):
        _, count = self.title.split(" ")
        count = int(count)
        global_cards = ComponentManager.get_component("draw")
        drawn = ""

        for _ in range(count + self.bonus):
            if not global_cards.cards:
                game_master._reshuffle_game_stack_into_draw_stack()

            random_card_uid = random.choice(list(global_cards.cards))
            random_card_obj = ComponentManager.get_uid_object(random_card_uid)
            random_card_obj.transfer_owner("draw", player.uid, forced=True, new_card=True)
            drawn += f"{Color.CYAN} got {random_card_obj.render()}{Color.CYAN} from stack\n"
        self.bonus = -1
        return drawn, None

    def __str__(self):
        past_render = super().__str__()
        _, count = self.title.split(" ")
        count = int(count)
        if self.bonus > count:
            past_render += f" {Color.CYAN}({Color.PINK}+{Color.CYAN}{self.bonus}){Color.RESET}"
        return past_render

class ReverseCard(JokerCard):
    def __init__(self, color:CardColor, title:str):
        super().__init__(color, title)
        
    def make_action(self, current_player, next_player):
        game_master = ComponentManager.get_component("game_master")
        if len(game_master.players) == 2:
            return f"{Color.CYAN}oh yeah... you again{Color.RESET}", None
        
        game_master.game_direction = 1 if game_master.game_direction == -1 else -1
        return f"{Color.CYAN}reversed direction :P{Color.RESET}", None

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
