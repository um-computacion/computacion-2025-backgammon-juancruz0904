from .board import Board
from .player import Player
from .dice import Dice

class BackgammonGame:
    def __init__(self, player1_name="Jugador 1", player2_name="Jugador 2"):
        self.board = Board()
        self.dice = Dice()
        self.player1 = Player(player1_name, color="white")
        self.player2 = Player(player2_name, color="black")
        self.current_player = self.player1
        self.is_game_over = False

    def start_game(self):
        # Indica quién comienza y hace el primer turno.
        pass

    def roll_dice(self):
        self.dice.roll()

    def get_valid_moves(self):
        # Indica cuales son los movimientos válidos del jugador actual.
        pass

    def make_move(self, start_point, end_point):
        # Indica como mover una ficha y permitir la jugada.
        pass

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_winner(self):
        # Indica si un jugador ha ganado.
        pass