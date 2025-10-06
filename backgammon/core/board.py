from .checker import Checker

class Point:
    def __init__(self):
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
    def __init__(self):
        # El tablero tiene 24 fichas
        self.points = {i: Point() for i in range(1, 25)}
        self.bar = {"white": [], "black": []}
        self.off_board = {"white": [], "black": []}
        self.setup_initial_positions()

    def setup_initial_positions(self):
        # Posisiones de las fichas en el tablero
        self.points[1].checkers.extend(["white"] * 2)
        self.points[6].checkers.extend(["black"] * 5)
        self.points[8].checkers.extend(["black"] * 3)
        self.points[12].checkers.extend(["white"] * 5)
        self.points[13].checkers.extend(["black"] * 5)
        self.points[17].checkers.extend(["white"] * 3)
        self.points[19].checkers.extend(["white"] * 5)
        self.points[24].checkers.extend(["black"] * 2)

    def send_to_bar(self, color):
        self.bar[color].append(color)

    def reenter_from_bar(self, color):
        if self.bar[color]:
            return self.bar[color].pop()
        return None