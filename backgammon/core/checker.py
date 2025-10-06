class Checker:
    """
    Representa una ficha individual en el juego de Backgammon.
    """
    def __init__(self, color: str):
        """
        Inicia una nueva ficha con un color.

        Argumentos:
            color (str): El color de la ficha, 'white' o 'black'.
        """
        if color not in ['white', 'black']:
            raise ValueError("El color de la ficha debe ser 'white' o 'black'.")
        self.color = color

    def __repr__(self) -> str:
        """
        Representación de cadena de la ficha para la depuración.
        """
        return f"Checker(color='{self.color}')"