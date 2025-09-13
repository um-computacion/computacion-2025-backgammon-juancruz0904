import unittest
from unittest.mock import patch
from io import StringIO

from backgammon.cli.main import display_board
from backgammon.core.board import Board

class MockPoint:
    def __init__(self, count, color):
        self._count = count
        self._color = color

    def count(self):
        return self._count

    def top_color(self):
        return self._color

class MockBoard:
    def __init__(self):
        self.points = {i: MockPoint(i % 3, 'white' if i % 2 == 0 else 'black') for i in range(1, 25)}
        self.bar = {'white': ['W'] * 2, 'black': ['B'] * 3}

class TestDisplayBoard(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_output(self, mock_stdout):
        board = MockBoard()
        display_board(board)
        output = mock_stdout.getvalue()

        # Verifica que se impriman ciertos elementos claves
        self.assertIn("Tablero de Backgammon", output)
        self.assertIn("Barra:", output)
        self.assertIn("Blancas: 2", output)
        self.assertIn("Negras: 3", output)
        self.assertIn("Punto 24:", output)
        self.assertIn("Punto  1:", output)

if __name__ == '__main__':
    unittest.main()