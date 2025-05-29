import curses
import random
import pathfinding
import time

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

        self.ranged_attackrate = 1.0  # Player attack cooldown in seconds
        self.melee_attackrate = 1.0  # Player attack cooldown in seconds
        self.magic_attackrate = 1.0  # Player magic attack cooldown in seconds
        self.last_attack_time = time.time()  # Initialize with the current time

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
        self.m_hitbase = (32 + int(round(self.strength / 2))) + ((self.level) * 5)
        self.r_hitbase = (32 + int(round(self.dexterity / 4))) + ((self.level) * 5)
        self.defense = self.armor_worn["protection"] - int(round(self.dexterity / 3)) * self.armor_worn["dexterity"]
        if self.shield_worn:
            self.ranged_weapon = None
            self.abilities.append("bash")
            self.defense -= self.shield_worn["protection"]
        else:
            if "abilities" in self.ranged_weapon:
                if "ranged_attack" in self.ranged_weapon["abilities"]:
                    self.abilities.append("ranged_attack")

        if "abilities" in self.melee_weapon:
            if "melee_attack" in self.melee_weapon["abilities"]:
                self.abilities.append("melee_attack")



    def create_character(self):
        self.type = "Squire"  # Keep the type as "Adventurer"
        self.abilities = ["bandage", "retreat"]  # Initialize abilities as a list

        # level: ["abilities"]
        # functionality to be as basic as possible and explained in another .py
        # abilities in most cases will be triggered automatically and always successful
        self.strength += 2
        self.constitution += 2
        self.outdoorsight = 10
        self.indoorsight = 6

        self.armor_worn = {
            "name": "Chainmail",
            "protection": -30,
            "type": "metal",
            "dexterity": 0,
            "magic": None
        }
        self.shield_worn = None
        self.melee_weapon = {
            "name": "LongSword",
            "damage": 3 + round(self.strength/6),
            "attackrate": 3,
            "attackper": 1,
            "type": "metal",
            "abilities": "melee_attack",
            "strength": 0,
            "magic": None,
            "target": "single"
        }

        self.ranged_weapon = {
            "name": "Crossbow",
            "damage": 3 + round(self.strength/6) - 1,
            "type": "wood",
            "strength": 0,
            "dexterity": 0,
            "range": round(self.strength/6)+round(self.dexterity/6),
            "attackrate": 5,
            "attackper": 1,
            "abilities": "ranged_attack",
            "magic": None,
            "target": "single"
        }


        self.recalculate_stats()


    def take_damage(self, damage):
        """Reduce player's HP when attacked."""
        print(f"PLAYER DAMAGE TAKEN! {damage}")
        print(f"PLAYER HEALTH! {self.health}")
        self.health -= damage
        if self.health <= 0:
            print("You have died!")
            return True
        return False

    def can_attack(self):
        """Check if the player can attack again."""
        return time.time() - self.last_attack_time >= self.attackrate

    def attack(self, monsters, monster, attack_type="melee", roll=None, combat_log=None):
        """Perform an attack if cooldown has expired."""
        if self.can_attack():
            if attack_type == "ranged":
                if roll <= self.r_hitbase:
                    combat_log.append(f"You fire at {monster.name}! (-{self.melee_attack} HP)")
                    if monster.take_damage(self.ranged_attack):
                        if monster.hp <= 0:
                            combat_log.append(f"{monster.name} is slain!")
                            monsters.remove(monster)
                else:
                    combat_log.append(f"You fire at {monster.name}! You MISS!)")
            elif attack_type == "melee":
                if roll <= self.m_hitbase:  # Example melee attack logic
                    combat_log.append(f"You strike {monster.name}! (-{self.melee_attack} HP)")
                    if monster.take_damage(self.melee_attack):
                        if monster.hp <= 0:
                            combat_log.append(f"{monster.name} is slain!")
                            monsters.remove(monster)
                else:
                    combat_log.append(f"You swing at {monster.name}! You MISS!)")

            self.last_attack_time = time.time()  # Reset attack timer

# curses.wrapper(display_player, player1)
