import curses
import random
import pathfinding

class Player:
    def __init__(self, name):
        self.name = name
        self.strength = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.dexterity = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.constitution = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.intelligence = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.wisdom = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.charisma = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1

        roll = random.randrange(0, 4)
        if roll == 0:
            self.type = "FTR"
            self.strength += 2
            self.constitution += 2
            self.outdoorsight = 6
            self.indoorsight = 3
            self.m_hitbase = 101
            self.r_hitbase = 76
        elif roll == 1:
            self.type = "THF"
            self.dexterity += 2
            self.charisma += 2
            self.outdoorsight = 12
            self.indoorsight = 5
            self.m_hitbase = 76
            self.r_hitbase = 101
        elif roll == 2:
            self.type = "ELF"
            self.dexterity += 2
            self.strength += 2
            self.outdoorsight = 12
            self.indoorsight = 8
            self.m_hitbase = 76
            self.r_hitbase = 126
        elif roll == 3:
            self.type = "DWF"
            self.constitution += 3
            self.strength += 1
            self.outdoorsight = 5
            self.indoorsight = 12
            self.m_hitbase = 101
            self.r_hitbase = 50
        self.attack = int(round(self.strength / 3)) + 1
        self.range = int(round(self.strength / 3)) + int(round(self.strength / 3)) + 1
        self.health = self.constitution * 3 + 1

    def take_damage(self, damage):
        """Reduce player's HP when attacked."""
        self.health -= damage
        if self.health <= 0:
            print("You have died!")
            return True
        return False

# curses.wrapper(display_player, player1)

def player_attack(monsters, grid, player_x, player_y, player, combat_log):
    """Allows the player to proactively attack monsters before they attack."""
    player_attack_range = 5  # Define player’s shooting range

    for monster in monsters[:]:  # Loop through monsters safely
        if pathfinding.has_line_of_sight(grid, player_x, player_y, monster.x, monster.y):
            distance = abs(monster.x - player_x) + abs(monster.y - player_y)

            # Player attacks ranged monsters within range
            if monster.behavior == "ranged" and distance <= player_attack_range:
                combat_log.append(f"You fire at {monster.name}! (-{player.attack} HP)")
                if monster.take_damage(player.attack):
                    combat_log.append(f"{monster.name} is slain!")
                    monsters.remove(monster)

            # Player can attack melee monsters **before they strike**
            elif monster.behavior == "melee" and distance == 1:  # Adjacent
                combat_log.append(f"You strike first at {monster.name}! (-{player.attack} HP)")
                if monster.take_damage(player.attack):
                    combat_log.append(f"{monster.name} is slain!")
                    monsters.remove(monster)
