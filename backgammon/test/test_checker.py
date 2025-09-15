import unittest
from backgammon.core.checker import Checker

class TestChecker(unittest.TestCase):

    def test_checker_creation_with_valid_color(self):
        """
        Verifica que se pueda crear una ficha con colores válidos.
        """
        white_checker = Checker('white')
        black_checker = Checker('black')

        self.assertEqual(white_checker.color, 'white')
        self.assertEqual(black_checker.color, 'black')

    def test_checker_creation_with_invalid_color(self):
        """
        Verifica que se lance un ValueError al intentar crear una ficha con un color no válido.
        """
        with self.assertRaises(ValueError) as cm:
            Checker('red')
        self.assertEqual(str(cm.exception), "El color de la ficha debe ser 'white' o 'black'.")

    def test_checker_representation(self):
        """
        Verifica la representación de cadena de la ficha.
        """
        white_checker = Checker('white')
        black_checker = Checker('black')

        self.assertEqual(repr(white_checker), "Checker(color='white')")
        self.assertEqual(repr(black_checker), "Checker(color='black')")

if __name__ == '__main__':
    unittest.main()