import unittest
from backgammon.core.board import Point, Board

class TestPoint(unittest.TestCase):
    def test_add_checker(self):
        p = Point()
        p.add_checker("white")
        self.assertEqual(p.count(), 1)
        self.assertEqual(p.top_color(), "white")

    def test_remove_checker(self):
        p = Point()
        p.add_checker("black")
        removed = p.remove_checker()
        self.assertEqual(removed, "black")
        self.assertEqual(p.count(), 0)

    def test_remove_checker_empty(self):
        p = Point()
        self.assertIsNone(p.remove_checker())

    def test_top_color_empty(self):
        p = Point()
        self.assertIsNone(p.top_color())

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_positions(self):
        self.assertEqual(self.board.points[1].count(), 2)
        self.assertEqual(self.board.points[6].count(), 5)
        self.assertEqual(self.board.points[8].count(), 3)
        self.assertEqual(self.board.points[12].count(), 5)
        self.assertEqual(self.board.points[13].count(), 5)
        self.assertEqual(self.board.points[17].count(), 3)
        self.assertEqual(self.board.points[19].count(), 5)
        self.assertEqual(self.board.points[24].count(), 2)

    def test_send_to_bar(self):
        self.board.send_to_bar("white")
        self.assertEqual(self.board.bar["white"], ["white"])

    def test_reenter_from_bar(self):
        self.board.send_to_bar("black")
        reentered = self.board.reenter_from_bar("black")
        self.assertEqual(reentered, "black")
        self.assertEqual(self.board.bar["black"], [])

    def test_reenter_from_empty_bar(self):
        self.assertIsNone(self.board.reenter_from_bar("white"))

if __name__ == "__main__":
    unittest.main()