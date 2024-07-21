"""
Entry point for the game and definitions for various classes.
"""

import secrets
import string

class UIDGenerator:
    """
    A class used to generate and store a unique 8-character alphanumeric UID.

    Attributes
    ----------
    uid : str
        Read-only property that returns the unique 8-character alphanumeric UID.
    """

    def __init__(self):
        """Initializes the UIDGenerator with a unique 8-character alphanumeric UID."""
        self.__uid = self._generate_8_char_alphanumeric_uid()

    @staticmethod
    def _generate_8_char_alphanumeric_uid():
        """
        Generates an 8-character alphanumeric UID.

        Returns
        -------
        str
            A string representing the unique 8-character alphanumeric UID.
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
            The unique 8-character alphanumeric UID.
        """
        return self.__uid

class Card:
    ...

class Player:
    ...

class GameMaster:
    ...

def main():
    """
    Entry point for the SquirrelUno project.
    """
    print("Welcome to the SquirrelUno project!")

if __name__ == "__main__":
    main()
