import unittest
from backgammon.core.game import BackgammonGame
from backgammon.core.board import Board

class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        self.game = BackgammonGame()
        self.game.start_game()

    def test_game_initialization(self):
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.current_player)
        self.assertFalse(self.game.is_game_over)

    def test_dice_roll(self):
        self.game.roll_dice()
        values = self.game.dice.get_values()
        self.assertIn(self.game.dice.die1, range(1, 7))
        self.assertIn(self.game.dice.die2, range(1, 7))
        self.assertTrue(len(values) in [2, 4])  # Doble o normal

    def test_valid_move(self):
        self.game.roll_dice()
        values = self.game.dice.get_values()
        # Simular un movimiento válido si el punto de inicio tiene fichas del jugador
        start = 24
        end = 24 - values[0]
        try:
            self.game.make_move(start, end, values[0])
        except Exception as e:
            self.fail(f"Movimiento válido falló con excepción: {e}")

    def test_invalid_move(self):
        self.game.roll_dice()
        with self.assertRaises(Exception):
            self.game.make_move(1, 1, 5)  # Movimiento inválido (sin desplazamiento)

    def test_switch_turn(self):
        current = self.game.current_player
        self.game.switch_turn()
        self.assertNotEqual(current, self.game.current_player)

if __name__ == "__main__":
    unittest.main()