API Documentation
=================


Overview
========

The SquirrelUno project is structured to facilitate easy understanding and extension. The core functionality is divided across several modules, each responsible for different aspects of the game. This documentation covers the primary entry points and key components of the project.

Console Entry Point
===================

The console entry point, defined in `__main__.py`, handles the command-line interface (CLI) for SquirrelUno. This module allows users to interact with the game through various commands and options.

.. automodule:: uno.__main__
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

Script Entry
============

The script entry point, defined in `__init__.py`, initializes the SquirrelUno package and contains the main logic for starting the game. This module ensures that all necessary components are correctly set up and ready to use.

.. automodule:: uno
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

Card Logic
==========

The `card_logic.py` module defines the different types of cards and their behaviors in the SquirrelUno game. This includes number cards, joker cards, and special action cards like draw and reverse cards.

.. automodule:: uno.card_logic
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

Game Logic
==========

The `game_logic.py` module manages the core game mechanics, including player actions, game flow, and turn management. It orchestrates the interactions between players and the deck of cards to simulate a game of Uno.

.. automodule:: uno.game_logic
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

Utilities
=========

The `utils.py` module provides utility functions and classes that support the main game logic, such as color codes for terminal output and unique identifier management.

.. automodule:: uno.utils
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:
