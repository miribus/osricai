import random
import pathfinding
import time

def check_and_resolve_player_combat(monsters, grid, player_x, player_y, player, combat_log, levelmap):
    """Allows the player to proactively attack monsters before they attack."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles
    player.chance = 0  # Initialize random modifier to hits

    dijkstra_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y, levelmap)

    for monster in monsters:  # Loop through monsters safely
        if levelmap.style == "indoor":
            player_attack_range = max(player.indoorsight, player.range)
            monster_attack_range = monster.indoorsight
        else:  # Outdoor
            player_attack_range = max(player.outdoorsight, player.range)
            monster_attack_range = monster.outdoorsight

        if pathfinding.has_line_of_sight(grid, player_x, player_y, monster.x, monster.y, levelmap, [monster.char for monster in monsters]):
            distance = max(abs(monster.x - player_x), abs(monster.y - player_y))

            # We should pause when the player has LoS to a monster
            # We'll need to add a list of monsters that the player can see
            # We'll need to enumerate visible monsters and their distances
            # We'll need to allow the player to choose which monster to attack
            # if the player has no ranged attack, melee attack is the only option
            # pausing until the player makes their choice, resuming combat after the choice is made
            # allowing further input when the player can attack again based on the attackrate of their last attack
            # for example if the player has a ranged attack, they can choose to attack a monster again after that weapon's attackrate has passed
            # The code below right now does not honor this at all, there is no pause, it all needs to be adjusted.

            # Player ranged attack
            if ("ranged_attack" in player.abilities or
                "magic_attack" in player.abilities) and player_attack_range >= distance >= 2:
                if player.can_attack() and distance <= player_attack_range:
                    if "ranged_attack" in player.abilities:
                        roll = random.randrange(1, 101)
                        combat_log.append(
                            f"DEBUG: Player Ranged Attack Roll: {roll}, Hit Base: {player.r_hitbase}, Chance Modifier: {player.chance}")
                        player.attackper(monsters, monster, "ranged", roll, combat_log)
                    player.last_attack_time = time.time()  # Reset player attack cooldown
            # Player melee attack
            elif ("melee_attack" in player.abilities or
                  "magic_attack" in player.abilities) and distance <= 1:
                if player.can_attack():  # Melee attack
                    if "melee_attack" in player.abilities:
                        roll = random.randrange(1, 101)
                        combat_log.append(f"DEBUG: Player Melee Attack Roll: {roll}, Hit Base: {player.m_hitbase}, Chance Modifier: {player.chance}")
                        player.attackper(monsters, monster, "melee", roll, combat_log)
                        player.last_attack_time = time.time()  # Reset player attack cooldown


def check_and_resolve_monster_combat(monsters, grid, player_x, player_y, player, combat_log, levelmap):
    """Allows monsters to attack the player."""
    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Orthogonal: Up, Down, Left, Right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal: NW, NE, SW, SE
    ]  # Adjacent tiles
    chance = 0  # Initialize random modifier to hits

    dijkstra_map = pathfinding.generate_dijkstra_map(grid, player_x, player_y, levelmap)

    for monster in monsters:  # Loop through monsters safely
        if levelmap.style == "indoor":
            player_attack_range = max(player.indoorsight, player.range)
            monster_attack_range = monster.indoorsight
        else:  # Outdoor
            player_attack_range = max(player.outdoorsight, player.range)
            monster_attack_range = monster.outdoorsight

        if pathfinding.has_line_of_sight(grid, player_x, player_y, monster.x, monster.y, levelmap, [monster.char for monster in monsters]):
            distance = max(abs(monster.x - player_x), abs(monster.y - player_y))

            # Monster attack
            if monster.behavior == "melee":
                monster_attack_range = 1
            if pathfinding.has_line_of_sight(grid, monster.x, monster.y, player_x, player_y, levelmap, [monster.char for monster in monsters]) and \
                    dijkstra_map[monster.y][monster.x] <= monster_attack_range:
                if monster.can_attack() and distance <= monster_attack_range:
                    monster.perform_attack(player)
                    combat_log.append(f"{monster.name} attacks you! (-{monster.damage} HP)")
                    monster.last_attack_time = time.time()  # Reset monster attack cooldown
                else:
                    roll = random.randrange(1, 101)
                    hit_chance = (monster.hitbase if monster.behavior == "melee" else monster.hitbase) - player.defense
                    combat_log.append(f"DEBUG: Monster Attack Roll: {roll}, Hit Base: {monster.hitbase}, Player Defense: {player.defense}, Final Hit Chance: {hit_chance}")
                    if roll in range(1, hit_chance):
                        damage = monster.damage
                        combat_log.append(f"{monster.name} attacks you! (-{damage} HP)")
                        player.take_damage(damage)
                    else:
                        combat_log.append(f"{monster.name} attacks you but MISSES!")
