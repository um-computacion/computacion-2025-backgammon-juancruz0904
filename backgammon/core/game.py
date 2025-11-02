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
        self.current_player = self.player1
        print(f"El juego comienza. Inicia el turno: {self.current_player.name} ({self.current_player.color.upper()})")

    def roll_dice(self):
        self.dice.roll_dice()

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def board_has_captured_checkers(self, color: str) -> bool:
        return len(self.board.bar.get(color, [])) > 0

    def is_valid_reentry(self, player_color: str, end_point: int, die_value: int) -> bool:
        """
        Verifica si la reentrada desde la barra al punto final es válida.
        """
        if player_color == 'white':
            if not (1 <= end_point <= 6):
                return False
            target_distance = 25 - end_point 
            if target_distance != die_value:
                return False
        else: # black
            if not (19 <= end_point <= 24):
                return False
            target_distance = end_point 
            if target_distance != die_value:
                return False

        end = self.board.points[end_point]
        return end.count() <= 1 or end.top_color() == player_color
    
    def is_valid_move(self, start_point: int, end_point: int, die_value: int) -> bool:
        """
        Verifica si un movimiento simple es válido.
        """
        player_color = self.current_player.color
        is_reentry_required = self.board_has_captured_checkers(player_color)
        
        if is_reentry_required:
            bar_point = 25 if player_color == 'black' else 0
            if start_point != bar_point:
                return False 
            
            return self.is_valid_reentry(player_color, end_point, die_value)

        if start_point in [0, 25]:
            return False

        if not (1 <= start_point <= 24):
            return False
            
        start = self.board.points[start_point]
        if start.count() == 0 or start.top_color() != player_color:
            return False

        if player_color == 'white':
            expected_end_point = start_point + die_value
            if 1 <= expected_end_point <= 24:
                if expected_end_point != end_point:
                    return False
            elif expected_end_point > 24:
                is_in_home_board = all(point_num > 18 for point_num in range(1, 25) if self.board.points[point_num].top_color() == 'white')
                
                if end_point != 25:
                    return False
                
                if not self.is_in_home_board(player_color):
                    return False
                
                if expected_end_point == 25:
                    pass 
                elif expected_end_point > 25:
                    if not self.is_furthest_checker(start_point, player_color):
                        return False

            else:
                return False 
        else: 
            expected_end_point = start_point - die_value
            if 1 <= expected_end_point <= 24:
                if expected_end_point != end_point:
                    return False
            elif expected_end_point < 1:
                is_in_home_board = all(point_num < 7 for point_num in range(1, 25) if self.board.points[point_num].top_color() == 'black')
                
                if end_point != 0:
                    return False
                
                if not self.is_in_home_board(player_color):
                    return False
                
                if expected_end_point == 0:
                    pass 
                elif expected_end_point < 0:
                    if not self.is_furthest_checker(start_point, player_color):
                        return False
            else:
                return False 

        if 1 <= end_point <= 24:
            end = self.board.points[end_point]
            if end.count() > 1 and end.top_color() != player_color:
                return False 
        
        return True

    def is_in_home_board(self, player_color):
        """Verifica si todas las fichas del jugador están en su cuadrante de casa."""
        if player_color == 'white':
            points_to_check = range(1, 19) 
        else: 
            points_to_check = range(7, 25) 
        
        for point_num in points_to_check:
            point = self.board.points[point_num]
            if point.count() > 0 and point.top_color() == player_color:
                return False
        
        if self.board_has_captured_checkers(player_color):
            return False
            
        return True
        
    def is_furthest_checker(self, start_point, player_color):
        """Verifica si la ficha en start_point es la más alejada del off board."""
        furthest = -1
        if player_color == 'white':
            for point_num in range(1, 25):
                point = self.board.points[point_num]
                if point.count() > 0 and point.top_color() == 'white':
                    if point_num < furthest or furthest == -1:
                         furthest = point_num
            return start_point == furthest
        else:
            for point_num in range(1, 25):
                point = self.board.points[point_num]
                if point.count() > 0 and point.top_color() == 'black':
                    if point_num > furthest:
                         furthest = point_num
            return start_point == furthest


    def get_valid_moves(self) -> list[tuple[int, int, int]]:
        """
        Calcula todos los movimientos válidos posibles dado el estado actual del juego y los dados.
        Retorna una lista de tuplas: (start_point, end_point, die_value_used)
        """
        valid_moves = []
        player_color = self.current_player.color
        available_rolls = self.dice.get_available_rolls()
        
        is_reentry_required = self.board_has_captured_checkers(player_color)
        
        start_points = []
        if is_reentry_required:
            start_points.append(25 if player_color == 'black' else 0)
        else:
            for i in range(1, 25):
                point = self.board.points[i]
                if point.count() > 0 and point.top_color() == player_color:
                    start_points.append(i)

        is_bearing_off = self.is_in_home_board(player_color)
        off_board_point = 25 if player_color == 'white' else 0
        
        for start_point in start_points:
            for die in available_rolls:
                if player_color == 'white':
                    end_point = start_point + die
                    if end_point > 24 and is_bearing_off:
                        end_point = off_board_point
                else: 
                    end_point = start_point - die
                    if end_point < 1 and is_bearing_off:
                        end_point = off_board_point
                
                if self.is_valid_move(start_point, end_point, die):
                    if (start_point, end_point, die) not in valid_moves:
                        valid_moves.append((start_point, end_point, die))

        return valid_moves

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

        self.dice.use_roll(die_value)
        
        return True
        
    def check_game_over(self):
        """Verifica si un jugador ha sacado todas sus fichas."""
        
        if len(self.board.off_board.get('white', [])) == 15:
            self.is_game_over = True
            return True, 'white'
        
        if len(self.board.off_board.get('black', [])) == 15:
            self.is_game_over = True
            return True, 'black'
            
        return False, None