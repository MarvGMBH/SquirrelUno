from __future__ import annotations
from card_logic import CardType, CardColor, Card, NumberCard, JokerCard, Stack
from utils import UIDObj
import random
import os


class Player(UIDObj):
    def __init__(self, name: str, game_position: int):
        super().__init__()
        self.name = name
        self.game_position = game_position
        self.hands = Stack(self.uid, {})

    @classmethod
    def get_uid(cls, name: str):
        for uid, player_obj in UIDObj.iterate(Player):
            if player_obj.name == name:
                return uid
        raise ValueError(f"No match for Player: {name}")

    def card_count(self):
        return len(self.hands.cards)


class GameMaster(UIDObj):
    def __init__(self, players: list):
        super().__init__()
        self.players = self._init_players(players)
        self.player_turn = Player.get_uid(players[0])
        self.global_stack = Stack("global", self._create_cards())
        UIDObj.stacks["global"] = self.global_stack
        self.draw_stack = Stack("draw", {})
        UIDObj.stacks["draw"] = self.draw_stack
        self.game_stack = Stack("game", {})
        UIDObj.stacks["game"] = self.game_stack

        self._initialize_game()

        self.game_direction = -1
        self.game_active = True
        self.skip_unlooked = False
        self.last_user_action = None
        self.drawn_this_turn = False

    def _initialize_game(self):
        print("Laying down first card...")
        self._lay_down_first_card()
        print("Giving players cards...")
        self._give_players_cards()
        print("Filling draw stack...")
        self._fill_draw_stack()

    def _lay_down_first_card(self):
        while True:
            random_card_uid = random.choice(list(self.global_stack.cards))
            random_card_obj = UIDObj.get(random_card_uid)

            if random_card_obj.card_type != CardType.joker:
                random_card_obj.transfer_owner("global", "game")
                break

    def _give_players_cards(self):
        for player in self.players.values():
            for _ in range(7):
                self._transfer_random_card("global", player.uid)

    def _fill_draw_stack(self):
        cards_tuple = tuple(self.global_stack.cards.values())
        for card in cards_tuple:
            card.transfer_owner("global", "draw")

    def _transfer_random_card(self, from_stack: str, to_stack: str):
        random_card_uid = random.choice(list(self.global_stack.cards))
        random_card_obj = UIDObj.get(random_card_uid)
        random_card_obj.transfer_owner(from_stack, to_stack)

    def _create_cards(self):
        cards = {}
        for color in CardColor:
            if color == CardColor.no_color:
                continue

            for number in range(1, 10):
                new_card = NumberCard(number, color)
                new_card.owner = "global"
                cards[new_card.uid] = new_card

            self._add_joker_cards(cards, color)

        return cards

    def _add_joker_cards(self, cards, color):
        draw_2 = JokerCard(color, "draw 2")
        draw_2.owner = "global"
        cards[draw_2.uid] = draw_2

        draw_4 = JokerCard(color, "draw 4")
        draw_4.owner = "global"
        cards[draw_4.uid] = draw_4

        draw_4_no_color = JokerCard(CardColor.no_color, "draw 4")
        draw_4_no_color.owner = "global"
        cards[draw_4_no_color.uid] = draw_4_no_color

    def _init_players(self, players: list):
        created_players = {}
        for index, player_name in enumerate(players):
            new_player = Player(player_name, index)
            created_players[new_player.uid] = new_player
        return created_players

    def get_players_for_cycle(self):
        current_player = self.players[self.player_turn]
        next_player_pos = self._get_next_player_position(current_player.game_position)
        next_player = next(player_obj for uid, player_obj in UIDObj.iterate(Player) if player_obj.game_position == next_player_pos)
        return current_player, next_player

    def _get_next_player_position(self, current_position):
        next_position = (current_position + self.game_direction) % len(self.players)
        return next_position

    def show_censor_part(self, player: Player):
        os.system("clear")
        print("#########################################")
        print("\n" * 6)
        print(f" Next player please: {player.name}")
        print("\n" * 6)
        print("#########################################")
        input("Press enter to continue")
        os.system("clear")

    def show_current_player_deck(self, player: Player):
        os.system("clear")
        others_hands = self._get_others_hands(player)

        print("=========================",
              f"Player turn: {player.name}",
              f"Top card: {self.game_stack.last_added_card}",
              f"Other players' decks:\n{others_hands}",
              f"On your hands:\n{player.hands}",
              sep="\n")

        return input(f"Choose your action:\n"
                     f"Enter a number from 1 to {len(player.hands.cards)} for the corresponding card in your deck,\n"
                     f"'draw' to take a card, or 'skip' to skip your turn (after drawing).\n"
                     f"What will it be, {player.name}?\nAction: ")

    def _get_others_hands(self, player: Player):
        others_hands = ""
        for _, other in UIDObj.iterate(Player):
            if other.uid != player.uid:
                others_hands += f"{other.name} {other.card_count()}\n"
        return others_hands

    def make_player_action(self, current_player, next_player, action: str):
        if action == "draw" and not self.drawn_this_turn:
            self._draw_card(current_player)
        elif action == "skip" and self.drawn_this_turn:
            self.last_user_action = "skip"
        elif action.isdecimal():
            self._play_card_action(current_player, next_player, action)
        else:
            self.last_user_action = "invalid"

        if self.last_user_action in ["invalid", "wrong-card"]:
            self._handle_invalid_action(current_player)

    def _handle_invalid_action(self, current_player):
        print(f"Invalid action: {self.last_user_action}")
        input("Press enter to continue.")
        self.show_current_player_deck(current_player)

    def _draw_card(self, current_player):
        draw_stack_len = len(self.draw_stack.cards)
        card = self.draw_stack.get_card_per_index(draw_stack_len - 1)
        card.transfer_owner("draw", current_player.uid)
        self.last_user_action = "draw"
        self.drawn_this_turn = True

    def _play_card_action(self, current_player, next_player, action):
        try:
            index = int(action)
        except ValueError:
            self.last_user_action = "invalid"
            return

        game_card = self.game_stack.last_added_card
        player_card = current_player.hands.get_card_per_index(index - 1)

        if self._is_valid_card_to_play(game_card, player_card):
            player_card.make_action(next_player)
            player_card.transfer_owner(current_player.uid, "game")
            self.last_user_action = "played-card"
            self.drawn_this_turn = False
        else:
            self.last_user_action = "wrong-card"

    def game_cycle(self):
        current_player, next_player = self.get_players_for_cycle()
        player_action = self.show_current_player_deck(current_player)
        self.make_player_action(current_player, next_player, player_action)
        if self.last_user_action not in ["invalid", "wrong-card", "error: already drawn this turn", "error: must draw before skipping"]:
            self.player_turn = next_player.uid
            self.show_censor_part(next_player)

    def start(self):
        while self.game_active:
            self.skip_unlooked = False
            self.last_user_action = None
            self.drawn_this_turn = False
            self.game_cycle()
