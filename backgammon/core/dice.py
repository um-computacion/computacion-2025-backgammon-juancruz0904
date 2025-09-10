import random

class Dice:
    def __init__(self):
        """ Ahora Inicializamos los dados. """
        self.die1 = 0
        self.die2 = 0
        self.rolls_left = 0

    def roll_single(self):
        return random.randint(1, 6)

    def roll(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)

        if self.die1 == self.die2:
            self.rolls_left = 4
        else:
            self.rolls_left = 2

        return (self.die1, self.die2)

    def get_values(self) -> list[int]:
        if self.die1 == self.die2:
            return [self.die1] * 4
        else:
            return [self.die1, self.die2]

    def use_roll(self, value: int) -> bool:
        if self.rolls_left > 0 and (value == self.die1 or value == self.die2):
            self.rolls_left -= 1
            return True
        return False

    def __repr__(self) -> str:
        return f"Dice(die1={self.die1}, die2={self.die2}, rolls_left={self.rolls_left})"