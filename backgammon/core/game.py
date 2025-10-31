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
        self.dice.roll_dice()

    def get_valid_moves(self):
        pass

        def is_valid_move(self, start_point: int, end_point: int, die_value: int) -> bool:
            player_color = self.current_player.color

            if self.has_checker_on_bar(self.current_player):
                is_bar_move = (start_point == 0 and player_color == "white") or \
                              (start_point == 25 and player_color == "black")

                if not is_bar_move:
                    return False

                if player_color == "white":
                    reentry_point = 0 + die_value
                else:
                    reentry_point = 25 - die_value

                if reentry_point != end_point:
                    return False 

                if end_point < 1 or end_point > 24:
                    return False 

                end_point_obj = self.board.points[end_point]
                if end_point_obj.count() >= 2 and end_point_obj.top_color() != player_color:
                    return False

                return True  

            if start_point < 1 or start_point > 24:
                return False 

            if self.board.points[start_point].count() == 0 or self.board.points[
                start_point].top_color() != player_color:
                return False

            expected_end_point = start_point + die_value if player_color == "white" else start_point - die_value

            if (end_point == 25 and player_color == "white") or (end_point == 0 and player_color == "black"):
                if not self.all_checkers_in_home_board(self.current_player):
                    return False  

                if expected_end_point == end_point:
                    return True

                if player_color == "white" and expected_end_point > end_point: 
                    if self.is_max_rear_checker(start_point, player_color):
                        return True

                if player_color == "black" and expected_end_point < end_point:
                    if self.is_max_rear_checker(start_point, player_color):
                        return True

                return False

            if expected_end_point != end_point:
                return False 

            if end_point < 1 or end_point > 24:
                return False

            end_point_obj = self.board.points[end_point]
            if end_point_obj.count() > 1 and end_point_obj.top_color() != player_color:
                return False

            return True

        def make_move(self, start_point: int, end_point: int, die_value: int) -> bool:
            player_color = self.current_player.color

            if not self.is_valid_move(start_point, end_point, die_value):
                return False

            checker = None
            if (start_point == 0 and player_color == "white") or (start_point == 25 and player_color == "black"):
                checker = self.board.reenter_from_bar(player_color)
            else:
                start = self.board.points[start_point]
                checker = start.remove_checker()

            if checker is None:
                return False  

            if (end_point == 25 and player_color == "white") or (end_point == 0 and player_color == "black"):
                self.board.off_board[player_color].append(checker)
            else:
                end = self.board.points[end_point]

                if end.count() == 1 and end.top_color() != player_color:
                    captured_color = end.remove_checker() 
                    self.board.send_to_bar(captured_color) 

                end.add_checker(player_color) 

            success = self.dice.use_roll(die_value)

            if len(self.board.off_board[player_color]) == 15:
                self.is_game_over = True
                print(f"🎉 ¡{self.current_player.name} ha ganado!")

            return True

        def has_checker_on_bar(self, player) -> bool:
            return len(self.board.bar[player.color]) > 0

        def all_checkers_in_home_board(self, player) -> bool:
            color = player.color

            if len(self.board.bar[color]) > 0:
                return False

            if color == "white":
                for i in range(1, 19):
                    if self.board.points[i].top_color() == color:
                        return False

            else:  
                for i in range(7, 25):
                    if self.board.points[i].top_color() == color:
                        return False
            return True

        def is_max_rear_checker(self, point: int, color: str) -> bool:
            """Verifica si el punto es el más lejano (más a la izquierda o más a la derecha)
               para el movimiento de retirada, lo que permite el overshooting."""

            if color == "white":
                for i in range(19, point):
                    if self.board.points[i].top_color() == color and self.board.points[i].count() > 0:
                        return False  
                return True 

            else: 
                for i in range(point + 1, 7):
                    if self.board.points[i].top_color() == color and self.board.points[i].count() > 0:
                        return False  
                return True 

        def roll_dice(self):
            self.dice.roll_dice()  

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