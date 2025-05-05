import curses
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.strength = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.dexterity = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.constitution = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.intelligence = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.wisdom = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.charisma = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.health = (random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1)*3



# curses.wrapper(display_player, player1)
