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
        while True:
            roll1 = self.dice.roll_single()
            roll2 = self.dice.roll_single()

            if roll1 > roll2:
                self.current_player = self.player1
                break
            elif roll2 > roll1:
                self.current_player = self.player2
                break
            else:
                pass

    def roll_dice(self):
        self.dice.roll()

    def get_valid_moves(self):

        pass

    def is_valid_move(self, start_point: int, end_point: int, die_value: int) -> bool:
        player_color = self.current_player.color

        if self.board.points[start_point].count() == 0 or self.board.points[start_point].top_color() != player_color:
            return False

        if abs(end_point - start_point) != die_value:
            return False

        end_point_obj = self.board.points[end_point]
        if end_point_obj.count() > 1 and end_point_obj.top_color() != player_color:
            return False

        return True

    def make_move(self, start_point: int, end_point: int,
                  die_value: int) -> bool:  
        if not self.is_valid_move(start_point, end_point, die_value):
            return False  

        start = self.board.points[start_point]
        end = self.board.points[end_point]

        if end.count() == 1 and end.top_color() != self.current_player.color:
            captured_color = end.remove_checker()
            self.board.send_to_bar(captured_color)


        checker = start.remove_checker()
        end.add_checker(checker)

        success = self.dice.use_roll(die_value)

        return True  

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_winner(self):

        pass

    def has_checker_on_bar(self, player):
        return len(self.board.bar[player.color]) > 0

    def get_valid_reentry_points(self, player):
        
        pass

if __name__ == "__main__":
    game = BackgammonGame()
    game.start_game()
    game.make_move(0, 5, 5)