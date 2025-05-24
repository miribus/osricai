import time

class Monster:
    def __init__(self, attackrate, melee_attack, ranged_attack):
        self.attackrate = attackrate  # Time in seconds before next attack
        self.melee_attack = melee_attack  # Number of melee rolls per attack cycle
        self.ranged_attack = ranged_attack  # Number of ranged rolls per attack cycle
        self.last_attack_time = 0  # Track last attack time

    def can_attack(self):
        """Check if enough time has passed since last attack."""
        return time.time() - self.last_attack_time >= self.attackrate

    def attack(self, player):
        """Perform attack if cooldown has expired."""
        if self.can_attack():
            for _ in range(self.melee_attack):  # Roll melee attacks
                player.take_damage(self.roll_damage())
            for _ in range(self.ranged_attack):  # Roll ranged attacks
                player.take_damage(self.roll_damage())
            self.last_attack_time = time.time()  # Reset attack timer


class Player:
    def __init__(self, attackrate):
        self.attackrate = attackrate  # Player attack cooldown
        self.last_attack_time = 0  # Track last attack time

    def can_attack(self):
        """Check if player can attack again."""
        return time.time() - self.last_attack_time >= self.attackrate

    def attack(self, monster):
        """Perform attack if cooldown has expired."""
        if self.can_attack():
            monster.take_damage(self.roll_damage())
            self.last_attack_time = time.time()  # Reset attack timer
