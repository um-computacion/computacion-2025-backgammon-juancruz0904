import unittest
from unittest.mock import MagicMock, patch

from backgammon.core.game import BackgammonGame
from backgammon.core.board import Board

class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        """Prepara un juego limpio antes de cada prueba."""
        self.game = BackgammonGame(player1_name="Blanco", player2_name="Negro")
        self.white_player = self.game.player1
        self.black_player = self.game.player2

        self.game.dice.die1 = 0
        self.game.dice.die2 = 0
        self.game.dice.rolls_left = 0

    @patch.object(Board, 'setup_initial_positions')
    def test_initialization(self, mock_setup):
        """Verifica que el juego se inicialice correctamente."""
        self.assertIsInstance(self.game.board, Board)
        self.assertEqual(self.game.player1.name, "Blanco")
        self.assertEqual(self.game.player2.color, "black")
        self.assertFalse(self.game.is_game_over)

    @patch('backgammon.core.dice.Dice.roll_single', side_effect=[6, 1])
    def test_start_game_white_starts(self, mock_roll):
        """Verifica que el jugador blanco comience si saca el dado más alto."""
        self.game.start_game()
        self.assertEqual(self.game.current_player, self.white_player)

    @patch('backgammon.core.dice.Dice.roll_single', side_effect=[3, 5])
    def test_start_game_black_starts(self, mock_roll):
        """Verifica que el jugador negro comience si saca el dado más alto."""
        self.game.start_game()
        self.assertEqual(self.game.current_player, self.black_player)

    @patch('backgammon.core.dice.Dice.roll_single', side_effect=[2, 2, 4, 1])
    def test_start_game_draw(self, mock_roll):
        """Verifica que se repita la tirada en caso de empate."""
        self.game.start_game() 
        self.assertEqual(self.game.current_player, self.white_player)
        self.assertEqual(mock_roll.call_count, 4) 

    def test_switch_turn(self):
        """Verifica que el turno cambie correctamente entre jugadores."""
        self.game.current_player = self.white_player
        self.game.switch_turn()
        self.assertEqual(self.game.current_player, self.black_player)
        self.game.switch_turn()
        self.assertEqual(self.game.current_player, self.white_player)

    def setup_move_state(self, current_player, die1, die2):
        """Configura el estado del juego para un movimiento controlado."""
        self.game.current_player = current_player
        self.game.dice.die1 = die1
        self.game.dice.die2 = die2
        self.game.dice.rolls_left = 2 

    def test_is_valid_move_normal_move(self):
        """Prueba un movimiento válido para el jugador actual (Blanco, P6 -> P11, dado 5)."""
 
        self.game.current_player = self.white_player

        is_valid = self.game.is_valid_move(start_point=6, end_point=11, die_value=5)
        self.assertTrue(is_valid)

    def test_is_valid_move_invalid_distance(self):
        """Prueba un movimiento donde la distancia no coincide con el dado."""
        self.game.current_player = self.white_player

        is_valid = self.game.is_valid_move(start_point=6, end_point=9, die_value=5)
        self.assertFalse(is_valid)

    def test_is_valid_move_no_checker_at_start(self):
        """Prueba mover desde un punto vacío (P23)."""
        self.game.current_player = self.white_player

        is_valid = self.game.is_valid_move(start_point=23, end_point=20, die_value=3)
        self.assertFalse(is_valid)

    def test_is_valid_move_blocked_by_opponent(self):
        """Prueba mover a un punto con 2 o más fichas del oponente."""
        self.game.current_player = self.white_player

        is_valid = self.game.is_valid_move(start_point=6, end_point=12, die_value=6)
        self.assertFalse(is_valid) 

    def test_make_move_normal(self):
        """Prueba un movimiento normal de ficha y consumo de dado."""
        self.setup_move_state(self.white_player, die1=5, die2=0)  

        initial_count_start = self.game.board.points[6].count()  
        initial_count_end = self.game.board.points[11].count()  

        success = self.game.make_move(start_point=6, end_point=11, die_value=5)

        self.assertTrue(success)
        self.assertEqual(self.game.board.points[6].count(), initial_count_start - 1)  
        self.assertEqual(self.game.board.points[11].count(), initial_count_end + 1)  
        self.assertEqual(self.game.dice.rolls_left, 1) 

    def test_make_move_with_capture(self):
        """Prueba un movimiento de captura que envía la ficha del oponente a la barra."""
        self.setup_move_state(self.black_player, die1=4, die2=0)  

        while self.game.board.points[20].count() > 0:
            self.game.board.points[20].remove_checker()

        self.game.board.points[19].remove_checker()
        self.game.board.points[20].add_checker("white")

        initial_count_start = self.game.board.points[24].count()  

        success = self.game.make_move(start_point=24, end_point=20, die_value=4)

        self.assertTrue(success)
        
        self.assertEqual(self.game.board.points[24].count(), initial_count_start - 1) 
        self.assertEqual(self.game.board.points[20].count(), 1) 
        self.assertEqual(self.game.board.points[20].top_color(), "black")

        self.assertEqual(len(self.game.board.bar["white"]), 1)
        self.assertEqual(self.game.dice.rolls_left, 1)  

    def test_make_move_invalid_move_no_effect(self):
        """Prueba que un movimiento inválido no cambie el tablero ni los dados."""
        self.setup_move_state(self.white_player, die1=1, die2=0)  

        initial_count_start = self.game.board.points[1].count()  
        initial_rolls_left = self.game.dice.rolls_left  

        success = self.game.make_move(start_point=1, end_point=19, die_value=1)

        self.assertFalse(success)
        
        self.assertEqual(self.game.board.points[1].count(), initial_count_start)
        
        self.assertEqual(self.game.dice.rolls_left, initial_rolls_left)


if __name__ == '__main__':
    unittest.main()