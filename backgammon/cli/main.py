from backgammon.core.game import BackgammonGame
from backgammon.core.board import Board

CHECKER_SYMBOLS = {
    "white": "●",  
    "black": "○"  
}

MAX_FICHAS_DISPLAY = 5

def format_point(board: Board, point_number: int, row: int, top_half: bool) -> str:
    """Formatea la representación de una fila específica de un punto."""
    point = board.points[point_number]
    count = point.count()
    color = point.top_color()
    symbol = CHECKER_SYMBOLS.get(color, ' ')

    if top_half:
        if count >= (MAX_FICHAS_DISPLAY - row):
            return f" {symbol} "
        elif count > MAX_FICHAS_DISPLAY and row == 0:
            return f"({count:2d})" if count >= 10 else f"({count} )"
        else:
            return "   "
    else:
        if count > row:
            return f" {symbol} "
        elif count > MAX_FICHAS_DISPLAY and row == (MAX_FICHAS_DISPLAY - 1):
            return f"({count:2d})" if count >= 10 else f"({count} )"
        else:
            return "   "

def display_board(board: Board):
    """
    Función para mostrar el tablero de juego de Backgammon en la consola
    con una estructura visual más clara.
    """
    W_BAR = len(board.bar["white"])
    B_BAR = len(board.bar["black"])

    print("\n" + "=" * 67)
    print("      13 14 15 16 17 18 |BAR| 19 20 21 22 23 24")
    print("      -----------------  ---  -----------------")

    for row in range(MAX_FICHAS_DISPLAY):
        line = "      "
        for i in range(13, 19):
            line += format_point(board, i, row, True)

        bar_symbol = CHECKER_SYMBOLS.get("black", ' ')
        bar_content = f" {bar_symbol} " if row < B_BAR else "   "
        if row == 0 and B_BAR > MAX_FICHAS_DISPLAY:
            bar_content = f"({B_BAR:2d})"

        line += bar_content + "   "

        for i in range(19, 25):
            line += format_point(board, i, row, True)

        print(line)

    print("      |=================|===|=================|")
    print(
        f"     | Fichas Off: N:{len(board.off_board['black']):2d} |   | Fichas Off: B:{len(board.off_board['white']):2d} |")
    print("      |=================|===|=================|")

    for row in range(MAX_FICHAS_DISPLAY - 1, -1, -1):
        line = "      "

        for i in range(12, 6, -1):
            line += format_point(board, i, row, False)

        bar_symbol = CHECKER_SYMBOLS.get("white", ' ')
        bar_content = f" {bar_symbol} " if row < W_BAR else "   "
        if row == (MAX_FICHAS_DISPLAY - 1) and W_BAR > MAX_FICHAS_DISPLAY:
            bar_content = f"({W_BAR:2d})"

        line += bar_content + "   "

        for i in range(6, 0, -1):
            line += format_point(board, i, row, False)

        print(line)

    print("      -----------------  ---  -----------------")
    print("      12 11 10 09 08 07 |BAR| 06 05 04 03 02 01")
    print("=" * 67)


def get_player_move(player_name: str) -> tuple[int, int]:
    """Pide al jugador que ingrese su movimiento (punto_inicio, valor_dado)."""
    print("\n--- INGRESO DE MOVIMIENTO ---")

    while True:
        try:
            start_input = input(f"{player_name}, ingrese punto de inicio (1-24) o 'R' para terminar turno: ").upper()
            if start_input == 'R':
                raise ValueError("Terminar Turno")

            start_point = int(start_input)
            if start_point < 1 or start_point > 24:
                raise ValueError
            break
        except ValueError as e:
            if str(e) == "Terminar Turno":
                raise e
            print("Entrada inválida. Ingrese un número de punto entre 1 y 24, o 'R'.")

    while True:
        try:
            die_value = int(input("Ingrese el valor del dado a usar: "))
            if die_value < 1 or die_value > 6:
                raise ValueError
            break
        except ValueError:
            print("Entrada inválida. Ingrese un valor de dado entre 1 y 6.")
    return start_point, die_value


def calculate_end_point(start_point: int, die_value: int, color: str) -> int:
    """Calcula el punto de destino basado en el color."""
    if color == "white":
        return start_point + die_value
    else:
        return start_point - die_value

if __name__ == "__main__":
    game = BackgammonGame("Alice", "Bob")
    game.start_game()
    current_player = game.current_player

    print(f"El jugador inicial es: {current_player.name} ({current_player.color})\n")

    while not game.is_game_over:
        game.roll_dice()
        dados_disponibles = game.dice.get_values()

        while game.dice.rolls_left > 0:

            print("\n" * 2)
            print("=" * 70)
            print(f"TURNO DE: {current_player.name} ({current_player.color})")
            print(f"DADOS DISPONIBLES: {dados_disponibles}")
            print(f"Movimientos restantes: {game.dice.rolls_left}")
            print("=" * 70)
            display_board(game.board)
            print("-" * 70)
            try:
                start_point, die_value = get_player_move(current_player.name)
            except ValueError:
                break
            if die_value not in dados_disponibles:
                print(f"ERROR: El dado de valor {die_value} no está disponible o ya fue usado.")
                continue

            end_point = calculate_end_point(start_point, die_value, current_player.color)

            move_successful = game.make_move(start_point, end_point, die_value)

            if move_successful:
                print(f"\n✅ MOVIMIENTO EXITOSO: {start_point} -> {end_point} (usando {die_value})")

                dados_disponibles = game.dice.get_values()
            else:
                print(
                    f"\n❌ MOVIMIENTO INVÁLIDO: No se puede mover de {start_point} a {end_point} con el dado {die_value}.")
        print("\n--- FIN DEL TURNO ---")
        game.switch_turn()
        current_player = game.current_player