from __future__ import annotations
from card_logic import (CardType,
                        CardColor,
                        Card,
                        NumberCard,
                        JokerCard,
                        DrawCard,
                        ReverseCard,
                        Stack)

from utils import UIDObject, ComponentManager, Color
import random
import os

class Player(UIDObject):
    """
    Represents a player in the game.
    """
    def __init__(self, name:str, game_position:int):
        """
        Initializes a player with a name and game position.

        Args:
            name (str): The name of the player.
            game_position (int): The position of the player in the game.
        """
        super().__init__()
        self.name = name
        self.game_position = game_position
        self.hands = Stack(self.uid, {}, sorted_stack=True)

    @classmethod
    def get_uid(cls, name: str):
        """
        Gets the UID of a player by name.

        Args:
            name (str): The name of the player.

        Returns:
            str: The UID of the player.
        """
        for uid, player_obj in ComponentManager.iterate_uid_objects(Player):
            if player_obj.name == name:
                return uid
        raise ValueError(f"No match for Player: {name}")

    def card_count(self):
        """
        Returns the count of cards in the player's hand.

        Returns:
            int: The number of cards in the player's hand.
        """
        return len(self.hands.cards)

class GameMaster(UIDObject):
    """
    Manages the overall game logic.
    """
    def __init__(self, players: list):
        """
        Initializes the GameMaster with a list of players.

        Args:
            players (list): A list of player names.
        """
        super().__init__()
        ComponentManager.register_component("game_master", self)
        self.players = self._init_players(players)
        self.player_turn = Player.get_uid(players[0])
        self.global_stack = Stack("global", self._create_cards())
        self.global_stack.shuffle_deck()
        ComponentManager.register_component("global", self.global_stack)
        self.draw_stack = Stack("draw", {})
        ComponentManager.register_component("draw", self.draw_stack)
        self.game_stack = Stack("game", {})
        ComponentManager.register_component("game", self.game_stack)

        self._initialize_game()

        self.game_direction = 1
        self.game_active = True
        self.last_user_action = None
        self.drawn_this_turn = False
        self.layed_this_turn = False
        self.player_actions = []
        self.messages_for_next_player = []

    def _initialize_game(self):
        """
        Initializes the game by laying down the first card, dealing cards to players, and filling the draw stack.
        """
        print(f"{Color.YELLOW}Setting up the game...{Color.RESET}")
        self._lay_down_first_card()
        print(f"{Color.GREEN}Dealing cards to players...{Color.RESET}")
        self._give_players_cards()
        print(f"{Color.CYAN}Preparing the draw stack...{Color.RESET}")
        self._fill_draw_stack()

    def _lay_down_first_card(self):
        """
        Lays down the first card of the game.
        """
        while True:
            random_card_uid = random.choice(list(self.global_stack.cards))
            random_card_obj = ComponentManager.get_uid_object(random_card_uid)

            if random_card_obj.card_type != CardType.JOKER:
                random_card_obj.transfer_owner("global", "draw")
                break

    def _give_players_cards(self):
        """
        Deals cards to players at the start of the game.
        """
        for player in self.players.values():
            for _ in range(7):
                self._transfer_random_card("global", player.uid)

    def _fill_draw_stack(self):
        """
        Fills the draw stack with cards from the global stack.
        """
        cards_tuple = tuple(self.global_stack.cards.values())
        for card in cards_tuple:
            card.transfer_owner("global", "game")

    def _transfer_random_card(self, from_stack: str, to_stack: str):
        """
        Transfers a random card from one stack to another.

        Args:
            from_stack (str): The source stack.
            to_stack (str): The destination stack.
        """
        random_card_uid = random.choice(list(self.global_stack.cards))
        random_card_obj = ComponentManager.get_uid_object(random_card_uid)
        random_card_obj.transfer_owner(from_stack, to_stack)

    def _create_cards(self):
        """
        Creates the initial set of cards for the game.

        Returns:
            dict[str, Card]: The created cards.
        """
        cards = {}
        for color in CardColor:
            if color == CardColor.NO_COLOR:
                continue

            for number in range(1, 10):
                new_card = NumberCard(number, color)
                new_card.owner = "global"
                cards[new_card.uid] = new_card

            self._add_joker_cards(cards, color)

        return cards

    def _add_joker_cards(self, cards, color):
        """
        Adds joker cards to the set of cards.

        Args:
            cards (dict[str, Card]): The set of cards.
            color (CardColor): The color of the joker cards.
        """
        draw_2 = DrawCard(color, "draw 2")
        draw_2.owner = "global"
        cards[draw_2.uid] = draw_2

        draw_4 = DrawCard(color, "draw 4")
        draw_4.owner = "global"
        cards[draw_4.uid] = draw_4
        
        card_reverse = ReverseCard(color, "reverse")
        card_reverse.owner = "global"
        cards[card_reverse.uid] = card_reverse

        draw_4_no_color = DrawCard(CardColor.NO_COLOR, "draw 4")
        draw_4_no_color.owner = "global"
        cards[draw_4_no_color.uid] = draw_4_no_color

    def _init_players(self, players: list):
        """
        Initializes player objects.

        Args:
            players (list): A list of player names.

        Returns:
            dict[str, Player]: The created players.
        """
        created_players = {}
        for index, player_name in enumerate(players):
            new_player = Player(player_name, index)
            created_players[new_player.uid] = new_player
        return created_players

    def get_players_for_cycle(self):
        """
        Gets the current and next player for the game cycle.

        Returns:
            Player: The current player.
            Player: The next player.
        """
        current_player = self.players[self.player_turn]
        next_player_pos = self._get_next_player_position(current_player.game_position)
        next_player = next(player_obj for uid, player_obj in ComponentManager.iterate_uid_objects(Player) if player_obj.game_position == next_player_pos)
        return current_player, next_player

    def _get_next_player_position(self, current_position):
        """
        Gets the position of the next player based on the current position.

        Args:
            current_position (int): The current player's position.

        Returns:
            int: The next player's position.
        """
        next_position = (current_position + self.game_direction) % len(self.players)
        return next_position

    def show_winner(self, winner: Player):
        """
        Displays the winner of the game.

        Args:
            winner (Player): The winning player.
        """
        os.system("clear")
        print(f"{Color.ORANGE}#############################################################{Color.RESET}")
        print(f"{Color.BG_GREEN}{' '*len('#############################################################')}\n{Color.RESET}" * 6, end="")
        win_str = f"{Color.DARK_GRAY}Player {Color.WHITE}{winner.name}{Color.DARK_GRAY} has conquered the game!{Color.RESET}"
        print(f"\r\r{Color.BG_GREEN}{win_str}{Color.BG_GREEN}{' '*(3*(len('#############################################################')-len(win_str)))}{Color.RESET}")
        print(f"{Color.BG_GREEN}{' '*len('#############################################################')}\n{Color.RESET}" * 6)
        print(f"{Color.ORANGE}#############################################################{Color.RESET}")
        input(f"{Color.MAGENTA}Press Enter to bask in the glory of the victor!{Color.RESET}")
        os.system("clear")

    def show_censor_part(self, player: Player):
        """
        Displays a pause screen between player turns.

        Args:
            player (Player): The next player.
        """
        os.system("clear")
        print(f"{Color.ORANGE}#############################################################{Color.RESET}")
        print("\n" * 6)
        print(f"{Color.LIGHT_YELLOW}Next player, please step up: {Color.LIGHT_RED}{player.name}{Color.RESET}")
        print("\n" * 6)
        print(f"{Color.ORANGE}#############################################################{Color.RESET}")
        input(f"{Color.MAGENTA}Press Enter to continue the chaos!{Color.RESET}")
        os.system("clear")

    def show_current_player_deck(self, player: Player):
        """
        Displays the current player's deck and actions.

        Args:
            player (Player): The current player.

        Returns:
            str: The player's chosen action.
        """
        os.system("clear")
        others_hands = self._get_others_hands(player)

        print(f"{Color.ORANGE}=================================================={Color.RESET}",
              f"{Color.LIGHT_YELLOW}It's your turn, {Color.LIGHT_RED}{player.name}{Color.LIGHT_YELLOW}!{Color.RESET}",
              f"{Color.LIGHT_YELLOW}Top card on the stack:{Color.RESET} {self.game_stack.last_added_card}",
              f"{Color.LIGHT_YELLOW}Rival players' decks:{Color.RESET}\n{others_hands}",
              f"{Color.LIGHT_WHITE}Your cards:{Color.RESET}\n{player.hands}",
              sep="\n")
        print("")
        for line in self.player_actions:
            print(line)
        print("")
        
        player_action = input(f"{Color.LIGHT_YELLOW}What will you do?\n"
                              f"{Color.LIGHT_YELLOW}Type a number from {Color.LIGHT_RED}1{Color.LIGHT_YELLOW} to {Color.LIGHT_RED}{len(player.hands.cards)}{Color.LIGHT_YELLOW} for the corresponding card in your hand,\n{Color.RESET}"
                              f"{Color.LIGHT_RED}draw{Color.LIGHT_YELLOW} to take a card, or {Color.LIGHT_RED}skip{Color.LIGHT_YELLOW} to pass your turn.\n{Color.RESET}"
                              f"{Color.LIGHT_YELLOW}Choose wisely, {Color.LIGHT_RED}{player.name}{Color.LIGHT_YELLOW}...\nAction: {Color.LIGHT_CYAN}")
        print(Color.RESET)
        return player_action
    
    def _get_others_hands(self, player: Player):
        """
        Gets the hands of other players.

        Args:
            player (Player): The current player.

        Returns:
            str: A string representation of other players' hands.
        """
        others_hands = []
        for _, other in ComponentManager.iterate_uid_objects(Player):
            if other.uid != player.uid:
                others_hands.append(f"  {other.name}: {other.card_count()} cards")
            else:
                others_hands.append(f">>{other.name}: {other.card_count()} cards")
                
        lenght_player = len(others_hands)#
        game_direction = self.game_direction
        for index, line in enumerate(others_hands):
            if index == 0 and game_direction == -1:
                others_hands[index] = r"/\ " + others_hands[index]
            elif index == lenght_player-1 and game_direction == 1:
                others_hands[index] = r"\/ " + others_hands[index]
            else:
                others_hands[index] = r"|| " + others_hands[index]
                
        return "\n".join(others_hands) + "\n"

    def make_player_action(self, current_player, next_player, action: str):
        """
        Makes the player's action.

        Args:
            current_player (Player): The current player.
            next_player (Player): The next player.
            action (str): The action chosen by the current player.
        """
        if action == "del":
            card = self.game_stack.last_added_card
            self.player_actions.append(f"{Color.BG_RED}{Color.WHITE}DELETED {card}{Color.RESET}")
            self.messages_for_next_player.append(f"{Color.BG_RED}{Color.WHITE}DELETED {card}{Color.RESET}")
            self.game_stack.remove_card(card)
            UIDObject.remove(card.uid)
            self.last_user_action = "dell"
            return
        if action == "draw" and not (self.drawn_this_turn or self.layed_this_turn):
            self._draw_card(current_player)
            return
        if action == "next" and (self.drawn_this_turn or self.layed_this_turn):
            self.last_user_action = "next"
            return
        if action.isdecimal() and not self.layed_this_turn:
            self._play_card_action(current_player, next_player, action)
            return

        self.last_user_action = f"Invalid action: {action}"
        self.show_current_player_deck(current_player)
        
    def _draw_card(self, current_player):
        """
        Draws a card for the current player.

        Args:
            current_player (Player): The current player.
        """
        draw_stack_len = len(self.draw_stack.cards)
        card = self.draw_stack.get_card_per_index(draw_stack_len - 1)
        card.transfer_owner("draw", current_player.uid, new_card=True)
        self.last_user_action = "draw"
        self.drawn_this_turn = True
        self.player_actions.append(f"{Color.CYAN}You drew {card.render()} {Color.CYAN}from the stack.{Color.RESET}")
        
    def _is_valid_card_to_play(self, game_card, player_card):
        """
        Checks if the player's card is valid to play.

        Args:
            game_card (Card): The top card on the game stack.
            player_card (Card): The card the player wants to play.

        Returns:
            bool: True if the card is valid to play, False otherwise.
        """
        if player_card.card_type == CardType.JOKER:
            return self._is_valid_joker_card(game_card, player_card)
        else:
            return self._is_valid_number_card(game_card, player_card)

    def _is_valid_joker_card(self, game_card, player_card):
        """
        Checks if the joker card is valid to play.

        Args:
            game_card (Card): The top card on the game stack.
            player_card (Card): The joker card the player wants to play.

        Returns:
            bool: True if the card is valid to play, False otherwise.
        """
        if player_card.color == CardColor.NO_COLOR:
            return True
        if game_card.card_type == CardType.JOKER:
            return game_card.color == CardColor.NO_COLOR or game_card.color == player_card.color
        return game_card.color == player_card.color

    def _is_valid_number_card(self, game_card, player_card):
        """
        Checks if the numbered card is valid to play.

        Args:
            game_card (Card): The top card on the game stack.
            player_card (Card): The numbered card the player wants to play.

        Returns:
            bool: True if the card is valid to play, False otherwise.
        """
        if game_card.card_type == CardType.JOKER:
            return False
        return game_card.color == player_card.color or game_card.number == player_card.number

    def _play_card_action(self, current_player, next_player, action):
        """
        Executes the action of playing a card.

        Args:
            current_player (Player): The current player.
            next_player (Player): The next player.
            action (str): The action chosen by the current player.
        """
        try:
            index = int(action)
        except ValueError:
            self.last_user_action = "invalid"
            self.player_actions.append(f"{Color.RED}'{action}' is not a valid move.{Color.RESET}")
            return

        game_card = self.game_stack.last_added_card
        player_card = current_player.hands.get_card_per_index(index - 1)
        action_response = None
        if self._is_valid_card_to_play(game_card, player_card):
            if player_card.card_type == CardType.JOKER:
                action_response, next_player_response = player_card.make_action(self.game_stack.last_added_card, current_player, next_player)
                if next_player_response is not None:
                    self.messages_for_next_player.append(next_player_response)
            player_card.transfer_owner(current_player.uid, "game")
            self.last_user_action = "played-card"
            if action_response is not None:
                self.player_actions.append(action_response)
            else:
                self.player_actions.append(f"{Color.GREEN}You played the card {player_card}")
            self.layed_this_turn = True
        else:
            self.last_user_action = "wrong-card"
            self.player_actions.append(f"{Color.RED}Your card {player_card} doesn't match the top card!{Color.RESET}")

    def check_winner(self):
        """
        Checks if there is a winner.

        Returns:
            Player: The winning player if there is a winner, None otherwise.
        """
        for uid, player in self.players.items():
            if len(player.hands.cards) == 0:
                self.show_winner(player)

    def game_cycle(self, first_round):
        """
        Executes a game cycle.

        Args:
            first_round (bool): If True, this is the first round of the game.
        """
        current_player, next_player = self.get_players_for_cycle()
        if first_round:
            self.show_censor_part(current_player)
        player_action = self.show_current_player_deck(current_player)
        self.make_player_action(current_player, next_player, player_action)
        if self.last_user_action == "next" and (self.drawn_this_turn or self.layed_this_turn):
            current_player.hands.clear_new_flag()
            self.drawn_this_turn = False
            self.layed_this_turn = False
            self.player_actions.clear()
            self.player_actions.extend(self.messages_for_next_player)
            self.messages_for_next_player.clear()
            self.player_turn = next_player.uid
            self.show_censor_part(next_player)

    def start(self):
        """
        Starts the game.
        """
        first_round = True
        while self.game_active:
            self.last_user_action = None
            if len(self.draw_stack.cards) < 10:
                first_card = self.game_stack.last_added_card
                self.game_stack.shuffle_deck()
                card_tuples = [(uid, card) for uid, card in self.game_stack.cards.items()]
                for uid, card in card_tuples:
                    card.transfer_owner("game", "draw")
                first_card.transfer_owner("draw", "game")
                self.game_stack.last_added_card = first_card
                
            self.game_cycle(first_round)
            first_round = False
