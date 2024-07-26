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
    """
    Enum for card types.6
    """
    NUMBER = "number"
    JOKER = "joker"

class CardColor(Enum):
    """
    Enum for card colors.
    """
    NO_COLOR = "no_color"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"

class Card(UIDObject):
    """
    Base class for all cards.
    """
    def __init__(self, card_type: CardType, color:CardColor):
        """
        Initializes the card with a type.
        """
        super().__init__()
        self.card_type = card_type
        self._color = color
        self.owner = None
        self._new_card = False

    def get_stack_based_on_owner(self, owner_uid: str):
        """
        Gets the stack based on the owner UID.

        Args:
            owner_uid (str): The UID of the owner.

        Returns:
            Stack: The stack owned by the owner UID.
        """
        for uid, stack_obj in ComponentManager.iterate_uid_objects(Stack):
            if stack_obj.owner == owner_uid:
                return stack_obj
        raise ValueError(f"No stack found for owner UID: {owner_uid}")

    def transfer_owner(self, owner_uid: str, other_uid: str, *, forced=False, new_card=False):
        """
        Transfers the card to a new owner.

        Args:
            owner_uid (str): The UID of the current owner.
            other_uid (str): The UID of the new owner.
            forced (bool, optional): If True, force the transfer. Defaults to False.
            new_card (bool, optional): If True, mark as new card. Defaults to False.
        """
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
        """
        Marks the card as new.
        """
        self._new_card = True
    
    def clear_new_flag(self):
        """
        Clears the new card flag.
        """
        self._new_card = False
        
    def make_action(self):
        """
        overwrite function
        """
        return None, None

    @property
    def color(self):
        return self._color
    
    def __str__(self):
        """
        String representation of the card.
        """
        new_tag = ""
        if self._new_card:
            new_tag = "NEW "
        return f"{new_tag}{self.card_type} {self.owner}"

class NumberCard(Card):
    """
    Represents a numbered card.
    """
    def __init__(self, number: int, color: CardColor):
        """
        Initializes a numbered card with a number and color.
        """
        super().__init__(CardType.NUMBER, color)
        self.__number = number

    @property
    def number(self):
        """
        Returns the number of the card.
        """
        return self.__number

    def render(self):
        """
        Renders the card with color.
        """
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
        """
        String representation of the numbered card.
        """
        new_tag = ""
        if self._new_card:
            new_tag = f"{Color.LIGHT_GREEN}NEW {Color.RESET}"

        return f"{new_tag}{self.render()}"

class JokerCard(Card):
    """
    Represents a joker card.
    """
    def __init__(self, color: CardColor, title: str):
        """
        Initializes a joker card with a color and title.
        """
        super().__init__(CardType.JOKER, color)
        self.__title = title

    def make_action(self, last_card, current_player, next_player):
        """
        Executes the action of the joker card.

        Args:
            last_card (Card): The last played card.
            current_player (Player): The current player.
            next_player (Player): The next player.

        Returns:
            str: Description of the action.
            None: Placeholder for additional action (if any).
        """
        return f"Action {last_card.render()} {current_player.name} vs {next_player.name}", None

    @property
    def title(self):
        """
        Returns the title of the joker card.
        """
        return self.__title
    
    def render(self):
        """
        Renders the joker card with color.
        """
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
        """
        String representation of the joker card.
        """
        new_tag = ""
        if self._new_card:
            new_tag = f"{Color.LIGHT_MAGENTA}NEW {Color.RESET}"
        
        return f"{new_tag}{self.render()}"

class DrawCard(JokerCard):
    """
    Represents a draw card (special type of joker card).
    """
    def __init__(self, color: CardColor, title: str):
        """
        Initializes a draw card with a color and title.
        """
        super().__init__(color, title)
        self.bonus = 0
    
    def make_action(self, last_card, current_player, next_player):
        """
        Executes the action of the draw card.

        Args:
            last_card (Card): The last played card.
            current_player (Player): The current player.
            next_player (Player): The next player.

        Returns:
            str: Description of the action.
            str: Description of cards drawn by next player.
        """
        game_master = ComponentManager.get_component("game_master")
        _, count = self.title.split(" ")
        count = int(count)
        global_cards = ComponentManager.get_component("draw")

        drawn = ""
        for _ in range(count + self.bonus):
            random_card_uid = random.choice(list(global_cards.cards))
            random_card_obj = ComponentManager.get_uid_object(random_card_uid)
            random_card_obj.transfer_owner("draw", next_player.uid, forced=True, new_card=True)
            drawn += f"{Color.CYAN}{next_player.name} drew {random_card_obj.render()}{Color.CYAN} from the stack\n"
            
        return f"{Color.LIGHT_YELLOW}You generously gave {next_player.name} more cards!{Color.RESET}", drawn

    def __str__(self):
        """
        String representation of the draw card.
        """
        past_render = super().__str__()
        if self.bonus > 0:
            past_render += f" {Color.CYAN}({Color.PINK}+{Color.CYAN}{self.bonus}){Color.RESET}"
        return past_render
    
class ReverseCard(JokerCard):
    """
    Represents a reverse card (special type of joker card).
    """
    def __init__(self, color: CardColor, title: str):
        """
        Initializes a reverse card with a color and title.
        """
        super().__init__(color, title)
        
    def make_action(self, last_card, current_player, next_player):
        """
        Executes the action of the reverse card.

        Args:
            last_card (Card): The last played card.
            current_player (Player): The current player.
            next_player (Player): The next player.

        Returns:
            str: Description of the action.
            None: Placeholder for additional action (if any).
        """
        game_master = ComponentManager.get_component("game_master")
        if len(game_master.players) == 2:
            return f"{Color.CYAN}Oh, it's still your turn, {current_player.name}!{Color.RESET}", None
        
        game_master.game_direction = 1 if game_master.game_direction == -1 else -1
        return f"{Color.CYAN}Game direction has been reversed!{Color.RESET}", None

class Stack(UIDObject):
    """
    Represents a stack of cards.
    """
    def __init__(self, owner: str, cards: dict[str, Card], sorted_stack=False):
        """
        Initializes a stack with an owner and cards.

        Args:
            owner (str): The owner of the stack.
            cards (dict[str, Card]): The cards in the stack.
            sorted_stack (bool, optional): If True, the stack is sorted. Defaults to False.
        """
        super().__init__()
        self.sorted_stack = sorted_stack
        card_list = cards.items()
        if sorted_stack:
            card_list = sorted(card_list, key=lambda item: item[1].color.value)
        self.cards = OrderedDict(card_list)
        self.owner = owner
        self.last_added_card = None
        
    def shuffle_deck(self, remain_last_card=False):
        """
        Shuffles the deck.

        Args:
            remain_last_card (bool, optional): If True, the last card remains in place. Defaults to False.
        """
        if remain_last_card:
            last_card_uid = self.last_added_card.uid
        
        items = list(self.cards.items())
        random.shuffle(items)
        self.cards = OrderedDict(items)
        
        if remain_last_card:
            last_card = self.cards.pop(last_card_uid)
            self.cards[last_card_uid] = last_card
    
    def clear_new_flag(self):
        """
        Clears the new card flag for all cards in the stack.
        """
        for uid, card_obj in self.cards.items():
            card_obj.clear_new_flag()

    def get_card_per_index(self, index: int):
        """
        Gets a card by index.

        Args:
            index (int): The index of the card.

        Returns:
            Card: The card at the specified index.
        """
        try:
            return list(self.cards.values())[index]
        except IndexError:
            raise ValueError(f"No card at index: {index}")

    def add_card(self, card_obj: Card, new_flag=False):
        """
        Adds a card to the stack.

        Args:
            card_obj (Card): The card to add.
            new_flag (bool, optional): If True, marks the card as new. Defaults to False.
        """
        if new_flag:
            card_obj.set_new_card()
        self.cards[card_obj.uid] = card_obj
        self.last_added_card = card_obj
        if self.sorted_stack:
            self.cards = OrderedDict(sorted(self.cards.items(), key=lambda item: item[1].color.value))

    def remove_card(self, card_obj: Card):
        """
        Removes a card from the stack.

        Args:
            card_obj (Card): The card to remove.
        """
        if card_obj.uid in self.cards:
            del self.cards[card_obj.uid]
        else:
            raise ValueError(f"Card with UID {card_obj.uid} not found in stack")

    def __str__(self):
        card_list = list(self.cards.values())
        num_cards = len(card_list)

        if num_cards <= 10:
            # Display cards vertically
            return "\n".join(f"{index + 1}: {card}" for index, card in enumerate(card_list))
        
        # Calculate the number of rows and columns needed for more than 10 cards
        rows = min(10, (num_cards + 3) // 4)
        columns = (num_cards + rows - 1) // rows

        # Determine the maximum length of card descriptions
        max_len = max(len(f"{index + 1}: {card}") for index, card in enumerate(card_list))

        result = []
        for i in range(rows):
            row = []
            for j in range(columns):
                index = i * columns + j
                if index < num_cards:
                    card_str = f"{index + 1}: {card_list[index]}"
                    row.append(f"{card_str:<{max_len}}")  # Left align with fixed width
                else:
                    row.append(" " * max_len)  # Fill empty spaces
            result.append(" | ".join(row))

        return "\n".join(result)
