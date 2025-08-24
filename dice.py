import random

class Dice:
    """
    Muestra los dados en el juego.
    """

    def __init__(self):
        """
        Inicia los dados.
        """
        self.die1 = 0
        self.die2 = 0
        self.rolls_left = 0

    def roll(self) -> tuple[int, int]:
        """
        Lanza los dos dados y muestra su valor.
        Si saca un doble, se obtienen cuatro movimientos.

        Returns:
            tuple[int, int]: Los valores de los dos dados.
        """
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)

        if self.die1 == self.die2:
            self.rolls_left = 4
        else:
            self.rolls_left = 2

        return (self.die1, self.die2)

    def get_values(self) -> list[int]:
        """
        Obtiene los valores de los dados disponibles para el movimiento.
        Si el lanzamiento es un doble, devuelve cuatro valores.

        Returns:
            list[int]: Una lista con los valores de los dados.
        """
        if self.die1 == self.die2:
            return [self.die1] * 4
        else:
            return [self.die1, self.die2]

    def use_roll(self, value: int) -> bool:
        """
        Marca un valor de dado como usado.

        Args:
            value (int): El valor del dado que se ha usado.

        Returns:
            bool: True si el valor fue usado, False si no estaba disponible.
        """
        if self.rolls_left > 0 and (value == self.die1 or value == self.die2):
            self.rolls_left -= 1
            return True
        return False

    def __repr__(self) -> str:
        """
        Representación de cadena de los dados para depuración.
        """
        return f"Dice(die1={self.die1}, die2={self.die2}, rolls_left={self.rolls_left})"