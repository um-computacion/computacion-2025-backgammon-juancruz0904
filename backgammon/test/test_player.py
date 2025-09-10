import unittest
from backgammon.core.player import Player

class TestPlayer(unittest.TestCase):

    def test_valid_player_creation_white(self):
        player = Player(name="Alice", color="white")
        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.color, "white")

    def test_valid_player_creation_black(self):
        player = Player(name="Bob", color="black")
        self.assertEqual(player.name, "Bob")
        self.assertEqual(player.color, "black")

    def test_invalid_color_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Player(name="Charlie", color="red")
        self.assertEqual(str(context.exception), "El color del jugador debe ser 'white' o 'black'.")

    def test_repr_output(self):
        player = Player(name="Dana", color="white")
        expected_repr = "Player(name='Dana', color='white')"
        self.assertEqual(repr(player), expected_repr)

if __name__== '_main_':
    unittest.main()