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
        self.health = (random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1)*3
        self.attack = int(round(self.strength/3))+1


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
