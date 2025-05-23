import random
import pathfinding

def check_and_resolve_player_combat(monsters, grid, player_x, player_y, player, combat_log, levelmap):
    """Allows the player to proactively attack monsters before they attack."""
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

            # Player ranged attack
            if ("ranged_attack" in player.abilities or
                "magic_attack" in player.abilities) and distance <= player_attack_range:
                if player_attack_range > player.indoorsight or player_attack_range > player.outdoorsight:
                    chance = -50

                roll = random.randrange(1, 101)
                if roll in range(1, player.r_hitbase + chance):
                    combat_log.append(f"You fire at {monster.name}! (-{player.melee_attack} HP)")
                    if monster.take_damage(player.melee_attack):
                        combat_log.append(f"{monster.name} is slain!")
                        monsters.remove(monster)
                        continue  # Skip to the next monster
                else:
                    combat_log.append(f"You fire at {monster.name}! You MISS!)")

            # Player melee attack
            elif ("melee_attack" in player.abilities or
                  "magic_attack" in player.abilities) and distance <= 1:
                roll = random.randrange(1, 101)
                if roll in range(1, player.m_hitbase):
                    combat_log.append(f"You strike first at {monster.name}! (-{player.melee_attack} HP)")
                    if monster.take_damage(player.melee_attack):
                        combat_log.append(f"{monster.name} is slain!")
                        monsters.remove(monster)
                        continue  # Skip to the next monster
                else:
                    combat_log.append(f"You swing at {monster.name}! You MISS!)")


def check_and_resolve_monster_combat(monsters, grid, player_x, player_y, player, combat_log, levelmap):
    """Allows the player to proactively attack monsters before they attack."""
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
                roll = random.randrange(1, 101)
                hit_chance = (monster.hitbase if monster.behavior == "melee" else monster.hitbase) - player.defense
                if roll in range(1, hit_chance):
                    damage = monster.damage
                    combat_log.append(f"{monster.name} attacks you! (-{damage} HP)")
                    player.take_damage(damage)
                else:
                    combat_log.append(f"{monster.name} attacks you but MISSES!")
