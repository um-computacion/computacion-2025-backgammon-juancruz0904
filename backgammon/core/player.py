import random

class Player:
    def __init__(self, name: str, color: str):
        if color not in ['white', 'black']:
            raise ValueError("El color del jugador debe ser 'white' o 'black'.")
        self.name = name
        self.color = color

    def __repr__(self) -> str:
        return f"Player(name='{self.name}', color='{self.color}')"

# Ejemplo de uso
player1 = Player(name="Jugador 1", color="white")
player2 = Player(name="Jugador 2", color="black")

print(player1)
print(player2)