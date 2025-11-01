import random

class Dice:
    def __init__(self):
        self.die1 = 0
        self.die2 = 0
        self.rolls_left = 0
        self.available_rolls = [] 

    def roll_dice(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)

        if self.die1 == self.die2:
            self.rolls_left = 4
            self.available_rolls = [self.die1] * 4
        else:
            self.rolls_left = 2
            self.available_rolls = [self.die1, self.die2] 

    def roll_single(self):
        return random.randint(1, 6)

    def roll(self):
        self.roll_dice()
        return (self.die1, self.die2)

    def get_values(self) -> list[int]:
        """ Retorna los valores originales para la visualización. """
        if self.die1 == self.die2:
            return [self.die1] * 4
        else:
            return [self.die1, self.die2]

    def get_available_rolls(self) -> list[int]:
        """ Método usado por game.py para saber qué movimientos quedan. """
        return self.available_rolls

    def use_roll(self, value: int) -> bool:
        """ Consume un dado del valor especificado de los rolls disponibles. """
        if value in self.available_rolls:
            self.available_rolls.remove(value) 
            self.rolls_left = len(self.available_rolls)
            return True
        return False