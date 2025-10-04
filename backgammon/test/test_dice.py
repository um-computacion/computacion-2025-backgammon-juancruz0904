import unittest
from backgammon.core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_roll_dice_values_in_range(self):
        for _ in range(100):
            self.dice.roll_dice()
            self.assertIn(self.dice.die1, range(1, 6))
            self.assertIn(self.dice.die2, range(1, 6))
            self.assertIn(self.dice.rolls_left, [2, 4])

    def test_roll_single_value_in_range(self):
        for _ in range(100):
            value = self.dice.roll_single()
            self.assertIn(value, range(1, 7))

    def test_roll_method_allows_out_of_range(self):
        for _ in range(100):
            die1, die2 = self.dice.roll()
            self.assertIn(die1, range(1, 7))
            self.assertIn(die2, range(1, 7))
            self.assertIn(self.dice.rolls_left, [2, 4])

    def test_get_values_for_doubles(self):
        self.dice.die1 = 4
        self.dice.die2 = 4
        values = self.dice.get_values()
        self.assertEqual(values, [4, 4, 4, 4])

    def test_get_values_for_non_doubles(self):
        self.dice.die1 = 3
        self.dice.die2 = 5
        values = self.dice.get_values()
        self.assertEqual(values, [3, 5])

    def test_use_roll_valid(self):
        self.dice.die1 = 2
        self.dice.die2 = 5
        self.dice.rolls_left = 2
        result = self.dice.use_roll(5)
        self.assertTrue(result)
        self.assertEqual(self.dice.rolls_left, 1)

    def test_use_roll_invalid(self):
        self.dice.die1 = 2
        self.dice.die2 = 5
        self.dice.rolls_left = 2
        result = self.dice.use_roll(6)
        self.assertFalse(result)
        self.assertEqual(self.dice.rolls_left, 2)

    def test_repr_format(self):
        self.dice.die1 = 1
        self.dice.die2 = 2
        self.dice.rolls_left = 3
        expected = "Dice(die1=1, die2=2, rolls_left=3)"
        self.assertEqual(repr(self.dice), expected)

if __name__ == "__main__":
    unittest.main()