"""
Entry point for the game and definitions for various classes.
"""

import secrets
import string

class UIDObj:
    """
    A class used to generate and store a unique 8-character alphanumeric UID.

    Attributes
    ----------
    uid : str
        Read-only property that returns the unique 8-character alphanumeric UID. :noindex:
    """

    def __init__(self):
        """Initializes the UIDObj with a unique 8-character alphanumeric UID. :noindex:"""
        self.__uid = self._generate_8_char_alphanumeric_uid()

    @staticmethod
    def _generate_8_char_alphanumeric_uid():
        """
        Generates an 8-character alphanumeric UID.

        Returns
        -------
        str
            A string representing the unique 8-character alphanumeric UID. :noindex:
        """
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(8))

    @property
    def uid(self):
        """
        Read-only property that returns the unique 8-character alphanumeric UID.

        Returns
        -------
        str
            The unique 8-character alphanumeric UID. :noindex:
        """
        return self.__uid

class Card:
    """
    A class representing a card in the Uno game.

    It has all base interactions for a card.

    Attributes
    ----------
    color : str
        The color of the card (e.g., red, yellow, green, blue).
    value : str
        The value or number of the card.
    """

    def __init__(self, color, value):
        """
        Initializes a card with a color and value.

        Parameters
        ----------
        color : str
            The color of the card.
        value : str
            The value or number of the card. :noindex:
        """
        self.color = color
        self.value = value

    def __repr__(self):
        """
        Returns a string representation of the card.

        Returns
        -------
        str
            A string representing the card's color and value. :noindex:
        """
        return f"{self.color} {self.value}"

class NumCard(Card):
    """
    The basic colored number card for Uno.

    Inherits from Card and represents a standard number card in the game.
    """

    def __init__(self, color, number):
        """
        Initializes a number card with a color and number.

        Parameters
        ----------
        color : str
            The color of the card.
        number : int
            The number on the card. :noindex:
        """
        super().__init__(color, str(number))

class JokerCard(Card):
    """
    A card with special events for the game.

    This class represents special cards like 'Wild' and 'Wild Draw Four'.
    """

    def __init__(self, value):
        """
        Initializes a joker card with a value.

        Parameters
        ----------
        value : str
            The value of the joker card (e.g., 'Wild', 'Wild Draw Four'). :noindex:
        """
        super().__init__('wild', value)

class Player(UIDObj):
    """
    A class representing a player in the Uno game.

    Inherits from UIDObj to provide a unique identifier for each player.

    Attributes
    ----------
    name : str
        The name of the player.
    hand : list of Card
        The cards held by the player.
    """

    def __init__(self, name):
        """
        Initializes a player with a name and an empty hand.

        Parameters
        ----------
        name : str
            The name of the player. :noindex:
        """
        super().__init__()
        self.name = name
        self.hand = []

    def draw_card(self, card):
        """
        Adds a card to the player's hand.

        Parameters
        ----------
        card : Card
            The card to add to the hand. :noindex:
        """
        self.hand.append(card)

    def show_hand(self):
        """
        Displays the cards in the player's hand.

        Returns
        -------
        str
            A string representation of the cards in the player's hand. :noindex:
        """
        return ', '.join(str(card) for card in self.hand)

class GameMaster:
    """
    A class responsible for managing the Uno game.

    Attributes
    ----------
    players : list of Player
        The players in the game.
    deck : list of Card
        The deck of cards used in the game.
    """

    def __init__(self):
        """Initializes the game master with an empty list of players and an empty deck. :noindex:"""
        self.players = []
        self.deck = []

    def add_player(self, player):
        """
        Adds a player to the game.

        Parameters
        ----------
        player : Player
            The player to add to the game. :noindex:
        """
        self.players.append(player)

    def create_deck(self):
        """Creates a standard Uno deck. :noindex:"""
        colors = ['red', 'yellow', 'green', 'blue']
        numbers = list(range(1, 10))
        self.deck = [NumCard(color, number) for color in colors for number in numbers]
        special_values = ['Skip', 'Reverse', 'Draw Two']
        self.deck.extend([Card(color, value) for color in colors for value in special_values])
        self.deck.extend([JokerCard('Wild'), JokerCard('Wild Draw Four')] * 4)

    def shuffle_deck(self):
        """Shuffles the deck of cards. :noindex:"""
        import random
        random.shuffle(self.deck)

def main():
    """
    Entry point for the SquirrelUno project. :noindex:
    """
    print("Welcome to the SquirrelUno project!")

if __name__ == "__main__":
    main()
