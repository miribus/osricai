import curses
import random
import pathfinding

class Player:
    def __init__(self, name, classtype=0, level=1):  # Default classtype to 0
        self.name = name
        self.level = level
        self.type = classtype  # Always set to 0
        self.strength = min(random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+3, 18)
        self.dexterity = min(random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+3, 18)
        self.constitution = min(random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+3, 18)
        self.intelligence = min(random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+3, 18)
        self.wisdom = min(random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+3, 18)
        self.charisma = min(random.randrange(1,6)+random.randrange(1,6)+random.randrange(1,6)+3, 18)

        self.abilities = []  # Ensure abilities is a list

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


    def level_up(self):
        self.health += int(round(self.constitution / 6)) + random.randrange(3, 8)
        self.m_hitbase += 5
        self.r_hitbase += 5
        self.level += 1


    def recalculate_stats(self):
        # Recalculate stats based on level and other factors
        self.melee_attack = int(round(self.strength / 3)) + int(round(self.level / 2)) + self.melee_weapon["damage"]
        self.ranged_attack = int(round(self.strength / 6)) + self.ranged_weapon["damage"]
        self.range = int(round(self.strength / 4)) + int(round(self.dexterity / 4))
        self.health = (self.constitution * 4) + (self.level * 6)
        self.m_hitbase = (32 + int(round(self.strength / 2))) + ((self.level-1) * 5)
        self.r_hitbase = (32 + int(round(self.dexterity / 4))) + ((self.level-1) * 5)
        self.defense = self.armor["protection"] - int(round(self.dexterity / 3))


    def create_character(self):
        self.type = "Adventurer"  # Keep the type as "Adventurer"
        self.abilities = ["bandage", "retreat"]  # Initialize abilities as a list

        # level: ["abilities"]
        # functionality to be as basic as possible and explained in another .py
        # abilities in most cases will be triggered automatically and always successful
        self.strength += 2
        self.constitution += 2
        self.outdoorsight = 8
        self.indoorsight = 4

        self.armor = {"name": "Chainmail", "protection": -30, "type": "metal", "dexterity": 0}
        self.melee_weapon = {"name": "LongSword", "damage": 3, "type": "metal", "abilities": "melee_attack"}
        if "abilities" in self.melee_weapon:
            if "melee_attack" in self.melee_weapon["abilities"]:
                self.abilities.append("melee_attack")
        self.ranged_weapon = {"name": "Crossbow", "damage": 3, "type": "slow", "strength": 0,
                              "range": self.indoorsight+round(self.dexterity/6), "abilities": "ranged_attack"}
        if "abilities" in self.ranged_weapon:
            if "ranged_attack" in self.ranged_weapon["abilities"]:
                self.abilities.append("ranged_attack")

        self.recalculate_stats()


    def take_damage(self, damage):
        """Reduce player's HP when attacked."""
        self.health -= damage
        if self.health <= 0:
            print("You have died!")
            return True
        return False

# curses.wrapper(display_player, player1)


