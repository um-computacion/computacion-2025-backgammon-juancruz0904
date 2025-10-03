import unittest
from unittest.mock import Mock, patch
import sys
from io import StringIO
from backgammon.cli.main import display_board, main

class MockPoint:
    def __init__(self, count, top_color):
        self._count = count
        self._top_color = top_color

    def count(self):
        return self._count

    def top_color(self):
        return self._top_color

class MockBoard:
    def __init__(self):

        self.points = {
            24: MockPoint(2, 'black'),
            1: MockPoint(2, 'white')
        }
        self.bar = {
            'white': [],
            'black': ['a', 'b']
        }

        for i in range(1, 25):
            if i not in self.points:
                self.points[i] = MockPoint(0, None)

class MockBackgammonGame:
    def __init__(self):
        self.board = MockBoard()
        self.current_player = Mock(name='player')
        self.is_game_over = False
        self.dice = Mock()
        self.dice.die1 = 1
        self.dice.die2 = 2
        self.dice.get_values.return_value = [1, 2]
        self.dice.rolls_left = 2

    def start_game(self):
        pass

    def roll_dice(self):
        pass

    def make_move(self, start, end, die_value):
        pass

    def switch_turn(self):
        pass

class TestCli(unittest.TestCase):
    def setUp(self):
        self.mock_board = MockBoard()

    def test_display_board(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        display_board(self.mock_board)

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("Tablero de Backgammon", output)
        self.assertIn("Punto 24:  2 fichas (black)", output)
        self.assertIn("Punto  1:  2 fichas (white)", output)
        self.assertIn("Barra:", output)
        self.assertIn("Blancas: 0", output)
        self.assertIn("Negras: 2", output)
        self.assertIn("-" * 50, output)

    @patch('backgammon.cli.main.BackgammonGame', new=MockBackgammonGame)
    @patch('backgammon.cli.main.input', side_effect=['', '', ''])
    @patch('backgammon.cli.main.print')
    def test_main_function_runs_without_error(self, mock_print, mock_input):
        try:
            main()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()