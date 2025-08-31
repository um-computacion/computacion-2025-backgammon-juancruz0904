from .board import Board
from .player import Player
from .dice import Dice

class BackgammonGame:
    def __init__(self, player1_name="Jugador 1", player2_name="Jugador 2"):
        self.board = Board()
        self.dice = Dice()
        self.player1 = Player(player1_name, color="white")
        self.player2 = Player(player2_name, color="black")
        self.current_player = self.player1
        self.is_game_over = False

    def start_game(self):
        print("Determinando quién comienza...")

        while True:
            roll1 = self.dice.roll_single()
            roll2 = self.dice.roll_single()

            print(f"{self.player1.name} tira: {roll1}")
            print(f"{self.player2.name} tira: {roll2}")

            if roll1 > roll2:
                self.current_player = self.player1
                print(f"{self.player1.name} comienza el juego.")
                break
            elif roll2 > roll1:
                self.current_player = self.player2
                print(f"{self.player2.name} comienza el juego.")
                break
            else:
                print("Empate. Se repite la tirada.")

    def roll_dice(self):
        self.dice.roll()

    def get_valid_moves(self):
        # Lógica para calcular movimientos válidos del jugador actual.
        pass

    def is_valid_move(self, start_point: int, end_point: int, die_value: int) -> bool:
        player_color = self.current_player.color

        # El punto de inicio debe tener una ficha del jugador actual
        if self.board.points[start_point].count() == 0 or self.board.points[start_point].top_color() != player_color:
            return False

        # La distancia de movimiento debe coincidir con el valor del dado
        if abs(end_point - start_point) != die_value:
            return False

        # El punto de destino no puede tener 2 o más fichas del oponente
        end_point_obj = self.board.points[end_point]
        if end_point_obj.count() > 1 and end_point_obj.top_color() != player_color:
            return False

        return True

    def make_move(self, start_point: int, end_point: int, die_value: int):
        if not self.is_valid_move(start_point, end_point, die_value):
            print("Movimiento inválido.")
            return

        start = self.board.points[start_point]
        end = self.board.points[end_point]

        # Captura si hay una sola ficha del oponente
        if end.count() == 1 and end.top_color() != self.current_player.color:
            captured_color = end.remove_checker()
            self.board.send_to_bar(captured_color)
            print(f"{self.current_player.name} captura una ficha {captured_color} en el punto {end_point}.")

        # Movimiento normal
        checker = start.remove_checker()
        end.add_checker(checker)
        print(f"{self.current_player.name} mueve ficha de {start_point} a {end_point}")

        # Usar el valor del dado
        self.dice.use_roll(die_value)

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_winner(self):
        # Lógica para determinar si un jugador ha ganado.
        pass

    def has_checker_on_bar(self, player):
        return len(self.board.bar[player.color]) > 0

    def get_valid_reentry_points(self, player):
        # Esto depende del color: white entra en puntos 0–5, black en 18–23
        # Podés agregar lógica para validar si el punto está libre o capturable
        pass

if __name__ == "__main__":