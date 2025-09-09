import unittest
from unittest.mock import MagicMock

class Point:
    def _init_(self):
        self.checkers = []

    def add_checker(self, color):
        self.checkers.append(color)

    def remove_checker(self):
        return self.checkers.pop() if self.checkers else None

    def top_color(self):
        return self.checkers[-1] if self.checkers else None

    def count(self):
        return len(self.checkers)

class Board:
    def _init_(self):
        # El tablero tiene 24 puntos
        self.points = {i: Point() for i in range(1, 25)}
        self.bar = {"white": [], "black": []}
        self.off_board = {"white": [], "black": []} # Asumimos que esta clase existe
        self.setup_initial_positions()

    def setup_initial_positions(self):
        # 2 fichas blancas en el punto 1
        self.points[1].checkers.extend(["white"] * 2)
        # 5 fichas negras en el punto 12
        self.points[12].checkers.extend(["black"] * 5)
        # 3 fichas negras en el punto 17
        self.points[17].checkers.extend(["black"] * 3)
        # 5 fichas blancas en el punto 19
        self.points[19].checkers.extend(["white"] * 5)
        # 5 fichas blancas en el punto 6
        self.points[6].checkers.extend(["white"] * 5)
        # 3 fichas blancas en el punto 8
        self.points[8].checkers.extend(["white"] * 3)
        # 5 fichas negras en el punto 13
        self.points[13].checkers.extend(["black"] * 5)
        # 2 fichas negras en el punto 24
        self.points[24].checkers.extend(["black"] * 2)

    def send_to_bar(self, color):
        self.bar[color].append(color)

    def reenter_from_bar(self, color):
        if self.bar[color]:
            return self.bar[color].pop()
        return None

class TestBoard(unittest.TestCase):

    def setUp(self):
        """Configura un nuevo objeto Board antes de cada test."""
        self.board = Board()

    def test_initial_board_setup(self):
        """Verifica que las posiciones iniciales del tablero estén correctas."""
        self.assertEqual(self.board.points[1].count(), 2)
        self.assertEqual(self.board.points[1].top_color(), "white")

        self.assertEqual(self.board.points[12].count(), 5)
        self.assertEqual(self.board.points[12].top_color(), "black")

        self.assertEqual(self.board.points[17].count(), 3)
        self.assertEqual(self.board.points[17].top_color(), "black")

        self.assertEqual(self.board.points[19].count(), 5)
        self.assertEqual(self.board.points[19].top_color(), "white")

        self.assertEqual(self.board.points[6].count(), 5)
        self.assertEqual(self.board.points[6].top_color(), "white")

        self.assertEqual(self.board.points[8].count(), 3)
        self.assertEqual(self.board.points[8].top_color(), "white")

        self.assertEqual(self.board.points[13].count(), 5)
        self.assertEqual(self.board.points[13].top_color(), "black")

        self.assertEqual(self.board.points[24].count(), 2)
        self.assertEqual(self.board.points[24].top_color(), "black")

        # Verifica que otros puntos estén vacíos
        for i in range(1, 25):
            if i not in [1, 12, 17, 19, 6, 8, 13, 24]:
                self.assertEqual(self.board.points[i].count(), 0)
                self.assertIsNone(self.board.points[i].top_color())

        self.assertEqual(self.board.bar["white"], [])
        self.assertEqual(self.board.bar["black"], [])
        self.assertEqual(self.board.off_board["white"], [])
        self.assertEqual(self.board.off_board["black"], [])

    def test_send_to_bar(self):
        """Verifica que una ficha se envía correctamente a la barra."""
        initial_bar_white_count = len(self.board.bar["white"])
        self.board.send_to_bar("white")
        self.assertEqual(len(self.board.bar["white"]), initial_bar_white_count + 1)
        self.assertEqual(self.board.bar["white"][-1], "white")

        initial_bar_black_count = len(self.board.bar["black"])
        self.board.send_to_bar("black")
        self.assertEqual(len(self.board.bar["black"]), initial_bar_black_count + 1)
        self.assertEqual(self.board.bar["black"][-1], "black")

    def test_reenter_from_bar_success(self):
        """Verifica que una ficha se puede reingresar de la barra."""
        self.board.bar["white"].append("white") # Añadimos una ficha manualmente para el test
        self.board.bar["white"].append("white")
        
        reentered_color = self.board.reenter_from_bar("white")
        self.assertEqual(reentered_color, "white")
        self.assertEqual(len(self.board.bar["white"]), 1) # Queda una ficha

        reentered_color = self.board.reenter_from_bar("white")
        self.assertEqual(reentered_color, "white")
        self.assertEqual(len(self.board.bar["white"]), 0) # Ya no quedan fichas

    def test_reenter_from_bar_empty(self):
        """Verifica que reintentar reingresar de una barra vacía devuelve None."""
        self.assertEqual(self.board.reenter_from_bar("white"), None)
        self.assertEqual(self.board.reenter_from_bar("black"), None)

if _name_ == '_main_':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
