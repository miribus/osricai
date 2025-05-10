import curses
import random
import pathfinding

class Player:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.strength = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.dexterity = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.constitution = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.intelligence = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.wisdom = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1
        self.charisma = random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+1

        # For the sake of continuity, a general explanation of these abilities below, details to be written in another module
        # "melee_attack" - general melee attacks, non-magical unless weapon is magic, resolved in that function
        # "ranged_attack" - general ranged attacks, non-magical unless weapon is magic
        # "magic_attack" - general magic attack, ranged
        # "bandage" - weak heal for fighters
        # "retreat" - damage-inducing withdrawal from melee combat (moving away from adjacent target)
        # "damage_resistance" - damage-reducing, non-magical, non-effects, but does include magic weapon bonuses
        # "magic_resistance" - generally magic_damage reducing or nullifying effects
        # "hide" - ability to be withdrawn from enemy line of site calculations (free movement)
        # "escape" - ability to withdraw from combat without taking damage
        # "dodge" - ability to nullify (non magic) damage without 'escaping'
        # "unlock" - ability to open a non-magical locked barrier
        # "smashdoor" - ability to open a non-magical locked barrier, while taking damage
        # "poison" - ability to reduce damage from poisons, nullify it, or deal poisonous damage
        # "find_secret" - will reveal any secrets (non-magical) within the room/hallway
        # "find_trap" - will reveal any traps deemed non-magical and nullify effect
        # "influence" - will have some determination on NPC and perhaps monster reactions
        # "charm" - will have significant determination on NPC and monster reactions
        # "know_tricks" - will reveal other unique detail not covered by secrets, or traps
        # "resistance" - generally, damage reduction (or nullification) to ALL effects
        # "magical" - generally a modifier for above items as well as a highly contextual subset of abilities and NPC modifications to be determined later.
        self.create_character()

    def create_character(self):
        roll = random.randrange(0, 5)
        if roll == 0:
            self.type = "FTR"
            self.strength += 2
            self.constitution += 2
            self.outdoorsight = 6
            self.indoorsight = 3
            self.m_hitbase = 101
            self.r_hitbase = 76
            self.attack = int(round(self.strength / 3)) + int(round(self.level / 2)) + 1
            self.range = int(round(self.strength / 3)) + int(round(self.strength / 3)) + 1
            # level: ["abilities"]
            # functionality to be as basic as possible and explained in another .py
            # abilities in most cases will be triggered automatically and always successful
            self.abilities = {
                1: [
                    "melee_attack",
                    "ranged_attack",
                    "bandage",
                    "retreat",
                    "smashdoor",
                    "damage_resistance"
                ]
            }
            self.health = self.constitution * 4 + 1
        elif roll == 1:
            self.type = "THF"
            self.dexterity += 2
            self.charisma += 2
            self.outdoorsight = 12
            self.indoorsight = 5
            self.m_hitbase = 76
            self.r_hitbase = 101
            self.attack = int(round(self.strength / 3)) + int(round(self.level / 4)) + 1
            self.range = int(round(self.strength / 3)) + int(round(self.strength / 3)) + 1
            self.abilities = {
                1: [
                    "melee_attack",
                    "range_attack",
                    "find_trap",
                    "hide",
                    "escape",
                    "unlock",
                    "poison",
                    "dodge"
                ]
            }
            self.health = self.constitution * 2 + 1
        elif roll == 2:
            self.type = "ELF"
            self.dexterity += 2
            self.strength += 2
            self.outdoorsight = 12
            self.indoorsight = 8
            self.m_hitbase = 76
            self.r_hitbase = 126
            self.attack = int(round(self.strength / 3)) + int(round(self.level / 4)) + 1
            self.range = int(round(self.strength / 3)) + int(round(self.strength / 3)) + 1
            self.abilities = {
                1: [
                    "melee_attack",
                    "range_attack",
                    "find_secret",
                    "hide",
                    "escape",
                    "influence",
                    "poison",
                    "magic_resist"
                ]
            }
            self.health = self.constitution * 2 + 1
        elif roll == 3:
            self.type = "DWF"
            self.constitution += 3
            self.strength += 1
            self.outdoorsight = 5
            self.indoorsight = 12
            self.m_hitbase = 101
            self.r_hitbase = 50
            self.attack = int(round(self.strength / 3)) + int(round(self.level / 3)) + 1
            self.range = int(round(self.strength / 3)) + int(round(self.strength / 3)) + 1
            self.abilities = {
                1: [
                    "melee_attack",
                    "hide",
                    "retreat",
                    "know_tricks",
                    "resistance",
                    "smashdoor",
                    "dodge"
                ]
            }
            self.health = self.constitution * 3 + 1
        elif roll == 4:
            self.type = "WIZ"
            self.intelligence += 3
            self.wisdom += 1
            self.charisma += 1
            self.outdoorsight = 5
            self.indoorsight = 12
            self.m_hitbase = 25
            self.r_hitbase = 101
            self.attack = int(round(self.intelligence / 3)) + int(round(self.wisdom / 5)) + int(round(self.level / 4)) + 1
            self.range = int(round(self.intelligence / 3)) + int(round(self.wisdom / 3)) + 1
            self.abilities = {
                1: [
                    "magic_attack",
                    "find_secret",
                    "escape",
                    "charm",
                    "know_tricks",
                    "magical",
                    "magic_resist"
                ]
            }
            self.health = self.constitution * 1 + 1

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
