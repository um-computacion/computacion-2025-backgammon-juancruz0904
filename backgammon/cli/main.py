from backgammon.core.game import BackgammonGame
from backgammon.core.board import Board

def display_board(board: Board):
    """
    Función para mostrar el tablero de juego en la consola.
    Esto es una representación muy básica, puedes mejorarla.
    """
    print("-" * 50)
    print("Tablero de Backgammon")
    print("-" * 50)
    for i in range(24, 12, -1):
        print(f"Punto {i:2d}: {board.points[i].count():2d} fichas ({board.points[i].top_color() or 'vacío'})")

    print("\nBarra:")
    print(f"  Blancas: {len(board.bar['white'])}")
    print(f"  Negras: {len(board.bar['black'])}")

    print("\n")
    for i in range(1, 13):
        print(f"Punto {i:2d}: {board.points[i].count():2d} fichas ({board.points[i].top_color() or 'vacío'})")
    print("-" * 50)

def main():
    """
    Función principal para el modo de línea de comandos.
    """
    game = BackgammonGame()
    print("¡Bienvenido a Backgammon!")
    game.start_game()
    current_player = game.current_player

    while not game.is_game_over:
        print(f"\n--- Turno de {current_player.name} ({current_player.color}) ---")

        # Tirar los dados
        input("Presiona Enter para lanzar los dados...")
        game.roll_dice()
        die_values = game.dice.get_values()
        print(f"Has lanzado: {game.dice.die1} y {game.dice.die2}. Movimientos disponibles: {die_values}")
        rolls_to_use = die_values.copy()

        # Bucle de movimientos de jugada
        while game.dice.rolls_left > 0:
            display_board(game.board)
            print(f"Movimientos restantes: {rolls_to_use}")

            try:
                move_input = input("Ingresa tu movimiento (punto de inicio y punto final, ej: '24 20'): ")
                if not move_input:
                    break  # Permite al jugador pasar su turno ahora

                start, end = map(int, move_input.split())

                # Determinar el valor del dado utilizado en esta jugada
                die_value_used = abs(start - end)
                if die_value_used in rolls_to_use:
                    game.make_move(start, end, die_value_used)
                    rolls_to_use.remove(die_value_used)
                else:
                    print(f"Movimiento no coincide con los dados disponibles. Los dados son: {rolls_to_use}")
            except (ValueError, IndexError):
                print("Entrada inválida. Asegúrate de ingresar dos números separados por un espacio.")
            except Exception as e:
                print(f"Error: {e}")

        # Cambiar de turno ahora
        game.switch_turn()
        current_player = game.current_player

    print("¡Fin del juego!")

if __name__ == "__main__":
    main()