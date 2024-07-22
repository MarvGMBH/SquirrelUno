from utils import UIDObj
from enum import Enum

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

class Stack(UIDObj):
    def __init__(self, owner:str, cards:dict[str:Card]):
        super().__init__()
        self.cards = cards
        self.owner = owner
    
    def __str__(self):
        output = ""
        sorted_cards = sorted(self.cards.items(), key=lambda item: item[1].color)
        for uid, card in sorted_cards:
            if card.card_type == CardType.number:
                output += f"{card.color} {card.number}\n"
            elif card.card_type == CardType.joker:
                card_color = (card.color+' ') if card.color != CardColor.no_color.value else ''
                output += f"{card_color}{card.title}\n"
        return output
    