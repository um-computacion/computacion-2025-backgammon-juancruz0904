from .checker import Checker

class Board:
    def __init__(self):
        
        self.points = {i: [] for i in range(1, 25)}
        self.bar = {"white": [], "black": []}
        self.off_board = {"white": [], "black": []}
        self.setup_initial_positions()

    def setup_initial_positions(self):
        
        pass

    def move_checker(self, start_point, end_point):
        
        pass