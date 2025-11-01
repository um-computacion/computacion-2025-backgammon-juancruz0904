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

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def board_has_captured_checkers(self, color: str) -> bool:
        return len(self.board.bar.get(color, [])) > 0

    def is_valid_reentry(self, player_color: str, end_point: int) -> bool:
        if not (1 <= end_point <= 24):
            return False

        end_point_obj = self.board.points.get(end_point)
        opponent_color = 'black' if player_color == 'white' else 'white'
        
        if end_point_obj and end_point_obj.count() >= 2 and end_point_obj.top_color() == opponent_color:
            return False 
            
        return True
    
    def can_bear_off(self, player_color: str) -> bool:
        """Verifica si todas las fichas del jugador están en su cuadrante de casa."""
        return self.board.count_checkers_outside_home(player_color) == 0

    def check_game_over(self) -> tuple[bool, str]:
        """Verifica si un jugador ha sacado todas sus fichas (15)."""
        if len(self.board.off_board['white']) == 15:
            self.is_game_over = True
            return True, "white"
        if len(self.board.off_board['black']) == 15:
            self.is_game_over = True
            return True, "black"
        return False, ""

    def get_valid_moves(self) -> list:
        valid_moves = []
        player_color = self.current_player.color
        dice_values = self.dice.get_available_rolls() 
        
        is_bar_occupied = self.board_has_captured_checkers(player_color)
        
        if is_bar_occupied:
            start_point = 0 if player_color == 'white' else 25
            
            for die_value in dice_values:
                
                if player_color == 'white':
                    end_point = start_point + die_value
                    if 1 <= end_point <= 6 and self.is_valid_reentry(player_color, end_point):
                        valid_moves.append((start_point, end_point, die_value))
                        
                elif player_color == 'black':
                    end_point = start_point - die_value
                    if 19 <= end_point <= 24 and self.is_valid_reentry(player_color, end_point):
                        valid_moves.append((start_point, end_point, die_value))
            
        else:
            is_bear_off_possible = self.can_bear_off(player_color)

            for start_point in range(1, 25):
                point = self.board.points[start_point]
                
                if point.count() > 0 and point.top_color() == player_color:
                    
                    for die_value in dice_values:
                        
                        if player_color == 'white':
                            end_point = start_point + die_value
                            
                            if end_point <= 24:
                                end_point_obj = self.board.points[end_point]
                                if end_point_obj.count() <= 1 or end_point_obj.top_color() == player_color:
                                    valid_moves.append((start_point, end_point, die_value))
                            
                            elif is_bear_off_possible and start_point >= 19:
                                distance_to_bear_off = 25 - start_point
                                
                                if die_value >= distance_to_bear_off:
                                    
                                    if distance_to_bear_off < die_value:
                                        is_furthest = True
                                        for p in range(19, start_point):
                                            if self.board.points[p].count() > 0 and self.board.points[p].top_color() == player_color:
                                                is_furthest = False
                                                break
                                        if is_furthest:
                                            valid_moves.append((start_point, 25, die_value))
                                    else:
                                        valid_moves.append((start_point, 25, die_value))
                                        
                        elif player_color == 'black':
                            end_point = start_point - die_value
                            
                            if end_point >= 1:
                                end_point_obj = self.board.points[end_point]
                                if end_point_obj.count() <= 1 or end_point_obj.top_color() == player_color:
                                    valid_moves.append((start_point, end_point, die_value))

                            elif is_bear_off_possible and start_point <= 6:
                                distance_to_bear_off = start_point - 0
                                
                                if die_value >= distance_to_bear_off:
                                    
                                    if distance_to_bear_off < die_value:
                                        is_furthest = True
                                        for p in range(start_point + 1, 7):
                                            if self.board.points[p].count() > 0 and self.board.points[p].top_color() == player_color:
                                                is_furthest = False
                                                break
                                        if is_furthest:
                                            valid_moves.append((start_point, 0, die_value))
                                    else:
                                        valid_moves.append((start_point, 0, die_value))

        return self._remove_duplicate_moves(valid_moves)

    def _remove_duplicate_moves(self, moves):
        return list(set(moves))

    def make_move(self, start_point: int, end_point: int, die_value: int) -> bool:
        
        if not self.is_valid_move(start_point, end_point, die_value):
            return False

        if end_point == 0 or end_point == 25:
            checker_color = self.board.points[start_point].remove_checker()
            self.board.off_board[checker_color].append(checker_color)
        
        elif start_point == 0 or start_point == 25:
            checker_color = self.board.bar[self.current_player.color].pop()
            
            end = self.board.points[end_point]
            if end.count() == 1 and end.top_color() != checker_color:
                captured_color = end.remove_checker()
                self.board.send_to_bar(captured_color)
            end.add_checker(checker_color)

        else:
            start = self.board.points[start_point]
            end = self.board.points[end_point]

            if end.count() == 1 and end.top_color() != self.current_player.color:
                captured_color = end.remove_checker()
                self.board.send_to_bar(captured_color)

            checker_color = start.remove_checker()
            end.add_checker(checker_color)

        success = self.dice.use_roll(die_value) 
        return success
    
    def is_valid_move(self, start_point: int, end_point: int, die_value: int) -> bool:
        valid_moves = self.get_valid_moves()
        return (start_point, end_point, die_value) in valid_moves