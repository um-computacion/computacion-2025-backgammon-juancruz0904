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
        self.points = {i: Point() for i in range(1, 25)}
        self.bar = {"white": [], "black": []} 
        self.off_board = {"white": [], "black": []} 
        self.setup_initial_positions()

    def setup_initial_positions(self):
        self.points[1].checkers.extend(["white"] * 2)
        self.points[6].checkers.extend(["black"] * 5)
        self.points[8].checkers.extend(["black"] * 3)
        self.points[12].checkers.extend(["white"] * 5)
        self.points[13].checkers.extend(["black"] * 5)
        self.points[17].checkers.extend(["white"] * 3)
        self.points[19].checkers.extend(["white"] * 5)
        self.points[24].checkers.extend(["black"] * 2)

    def send_to_bar(self, color):
        """Mueve una ficha a la barra."""
        self.bar[color].append(color)

    def count_checkers_outside_home(self, color: str) -> int:
        """Cuenta el total de fichas que no están en el cuadrante de casa ni fuera del tablero."""
        count = 0
        
        count += len(self.bar.get(color, []))
        
        if color == 'white':
            for point_num in range(1, 19):
                point = self.points[point_num]
                if point.count() > 0 and point.top_color() == 'white':
                    count += point.count()
        else:
            for point_num in range(7, 25):
                point = self.points[point_num]
                if point.count() > 0 and point.top_color() == 'black':
                    count += point.count()
                    
        return count

    @property
    def pos(self):
        """Retorna una lista de 24 elementos (0-23) para la UI gráfica."""
        board_state = [None] * 24

        for point_number, point in self.points.items():
            if point.count() > 0:
                idx = point_number - 1
                board_state[idx] = (point.top_color(), point.count())
        return board_state