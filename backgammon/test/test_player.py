import unittest
from backgammon.core.player import Player 

class TestPlayer(unittest.TestCase):

    def test_player_creation_valid(self):
        """
        Prueba la creación de un jugador con colores válidos.
        """
        player_white = Player(name="Alice", color="white")
        self.assertEqual(player_white.name, "Alice")
        self.assertEqual(player_white.color, "white")

        player_black = Player(name="Bob", color="black")
        self.assertEqual(player_black.name, "Bob")
        self.assertEqual(player_black.color, "black")

    def test_player_creation_invalid_color(self):
        """
        Prueba que la creación de un jugador falle con un color inválido.
        """
        with self.assertRaisesRegex(ValueError, "El color del jugador debe ser 'white' o 'black'."):
            Player(name="Charlie", color="red")

    def test_player_representation(self):
        """
        Prueba la representación de cadena (__repr__) del jugador.
        """
        player = Player(name="David", color="white")
        expected_repr = "Player(name='David', color='white')"
        self.assertEqual(repr(player), expected_repr)

    def test_player_name_attribute(self):
        """
        Prueba que el atributo 'name' se guarda correctamente.
        """
        player = Player(name="Eve", color="black")
        self.assertEqual(player.name, "Eve")

    def test_player_color_attribute(self):
        """
        Prueba que el atributo 'color' se guarda correctamente.
        """
        player = Player(name="Frank", color="white")
        self.assertEqual(player.color, "white")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)